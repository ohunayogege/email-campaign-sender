import os
import random
from tempfile import NamedTemporaryFile
from django.core.mail import get_connection, EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import time
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth.hashers import make_password, check_password
import pdfkit
from utils.function import generate_random_digits
from web.forms import CampaignForm, ContactForm, ContactListForm, SMTPForm, SegmentForm, SettingsForm
from web.tasks import send_campaign_email_task
from web.utils import get_random_sender_info, replace_tags
from .models import Campaign, Contact, ContactList, FailedContact, SMTPSetting, Segment, SentContact, Settings, User
from datetime import datetime, timedelta

def create_user_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_id = f"BITBIZ_{generate_random_digits(4)}"
        user = User.objects.create_user(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
        user.set_password(settings.DEFAULT_PASSWORD)
        user.save()
        msg = {"status": True, "message": f"The User ID is {user_id}"}
        return JsonResponse(msg)
    return render(request, 'create_user.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = settings.DEFAULT_PASSWORD
        user = authenticate(username=user_id, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': True, 'message': 'Please wait while we redirect you to the dashboard'})
        else:
            return JsonResponse({'status': False, 'message': 'Invalid user ID'})
    return render(request, 'login.html')


def dashboard_view(request):
    # Let's create the Settings if not exists
    if not Settings.objects.exists():
        Settings.objects.create(
            email_tag='[[Email]]',
            name_tag='[[Name]]',
            time_tag='[[Time]]',
            date_tag='[[Date]]',
            clock_type='Analog'
        )
        return redirect("dashboard")
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    ctx = {
        'clock_type': clock_type,
    }
    return render(request, 'dashboard.html', ctx)

def contact_view(request):
    segments = Segment.objects.all()
    contacts = Contact.objects.all()
    now = timezone.now()
    # Calculate the time 12 hours ago from now
    last_12_hours = now - timezone.timedelta(hours=12)
    # Count contacts added within the last 12 hours
    new_contacts_count = Contact.objects.filter(created_at__gte=last_12_hours).count()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    ctx = {
        "segments": segments,
        "all_contacts": contacts,
        'new_contacts_count': new_contacts_count,
        'clock_type': clock_type,
    }
    return render(request, 'contact_view.html', ctx)


def contact_list(request):
    contacts = Contact.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    return render(request, 'contact_list.html', {'contacts': contacts, 'clock_type': clock_type,})

# def contact_detail(request, pk):
#     contact = get_object_or_404(Contact, pk=pk)
#     return render(request, 'contact_detail.html', {'contact': contact})


def delete_all_contacts(request):
    if request.method == 'POST':
        Contact.objects.all().delete()
        # msg = {"status": True, "message": "All contacts have been deleted successfully."}
        # return JsonResponse(msg)
    return redirect('contacts_page')

def add_contact(request):
    segments = Segment.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    if request.method == 'POST':
        segment = request.POST['segment']
        name = request.POST['name']
        email = request.POST['email']
        segment = Segment.objects.get(pk=segment)
        # Check if the contact exists
        if Contact.objects.filter(email=email, segment=segment).exists():
            return JsonResponse({'status': False, 'message': 'Contact already exists'})
        Contact.objects.create(name=name, email=email, segment=segment)
        msg = {"status": True, "message": "Contact created successfully"}
        return JsonResponse(msg)
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form,"segments": segments, 'clock_type': clock_type,})

def contact_create(request):
    segments = Segment.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    if request.method == 'POST':
        segment_id = request.POST['segment']
        file = request.FILES['file']
        
        # Check if the segment exists
        try:
            segment = Segment.objects.get(pk=segment_id)
        except Segment.DoesNotExist:
            msg = {"status": False, "message": "Segment does not exist"}
            return JsonResponse(msg)

        # Process the uploaded file
        for line in file:
            try:
                email = line.decode().strip()
                print(email)
            except ValueError:
                # Skip lines that don't contain exactly two values
                continue

            # Check if the email already exists
            if Contact.objects.filter(email=email, segment=segment).exists():
                continue

            # Create the contact
            name = email.split('@')[0]
            Contact.objects.create(name=name, email=email, segment=segment)
        
        msg = {"status": True, "message": "Contacts uploaded successfully"}
        return JsonResponse(msg)
    else:
        form = ContactForm()
    
    return render(request, 'contact_form.html', {'form': form, 'segments': segments, 'clock_type': clock_type,})


def contact_delete(request):
    if request.method == 'POST':
        Contact.objects.all().delete()
        msg = {"status": True, "message": "Contacts has been deleted successfully."}
        return JsonResponse(msg)
        # return redirect('contact-list')
    return render(request, 'contact_confirm_delete.html')

def delete_contact(request, contact_id):
    if request.method == 'POST':
        contact = get_object_or_404(Contact, id=contact_id)
        contact.delete()
        msg = {"status": True, "message": "Contact has been deleted successfully."}
        return JsonResponse(msg)
    return JsonResponse({"status": False, "message": "Invalid request."})

# Segments
def segment_list(request):
    segments = Segment.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    return render(request, 'segment_list.html', {'segments': segments, 'clock_type': clock_type,})

def segment_detail(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    # Let's get the contacts in this segment
    contacts = Contact.objects.filter(segment=segment)
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    return render(request, 'segment_detail.html', {'segment': segment, 'contacts': contacts, 'clock_type': clock_type,})

def delete_segment(request, segment_id):
    if request.method == 'POST':
        segment = get_object_or_404(Segment, id=segment_id)
        segment.delete()
        msg = {"status": True, "message": "Segment has been deleted successfully."}
        return JsonResponse(msg)
    return JsonResponse({"status": False, "message": "Invalid request."})

def segment_create(request):
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    if request.method == 'POST':
        segment_id = request.POST.get('id')  # Get the ID from the POST data
        name = request.POST['name']
        if segment_id:
            name = name.strip()
            # Check if the segment exists and that the segment is not the same name as the current segment.
            if Segment.objects.filter(name=name).exclude(pk=segment_id).exists():
                return JsonResponse({'status': False, 'message': 'Segment already exists'})
            segment = get_object_or_404(Segment, pk=segment_id)
            segment.name = name
            segment.save()
            msg = {"status": True, "message": "Segment updated successfully"}
            return JsonResponse(msg)
        else:
            # Check if the segment exists
            if Segment.objects.filter(name=name).exists():
                return JsonResponse({'status': False, 'message': 'Segment already exists'})
            Segment.objects.create(name=name)
            msg = {"status": True, "message": "Segment created successfully"}
            return JsonResponse(msg)
    else:
        segment_id = request.GET.get('id')
        if segment_id:
            segment = get_object_or_404(Segment, pk=segment_id)
            form = SegmentForm(initial={
                'name': segment.name
            })
            form_title = 'Update Segment'
        else:
            form = SegmentForm()
            form_title = 'Add Segment'
        ctx = {
            'form': form,
            'form_title': form_title,
            'segment': segment if segment_id else None,
            'clock_type': clock_type,
        }
    return render(request, 'segment_form.html', ctx)




def SMTPPage(request):
    smtp_settings = SMTPSetting.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    ctx = {
        "smtp_settings": smtp_settings,
        'clock_type': clock_type,
    }
    return render(request, 'smtp.html', ctx)

def AddUpdateSMTP(request):
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    if request.method == 'POST':
        form = SMTPForm(request.POST)
        if form.is_valid():
            smtp_id = request.POST.get('id')  # Get the ID from the POST data
            if smtp_id:
                # Update existing SMTP setting
                smtp_setting = get_object_or_404(SMTPSetting, pk=smtp_id)
                smtp_setting.host = form.cleaned_data['host']
                smtp_setting.port = form.cleaned_data['port']
                smtp_setting.username = form.cleaned_data['username']
                smtp_setting.password = form.cleaned_data['password']
                smtp_setting.sender_name = form.cleaned_data['sender_name']
                smtp_setting.sender_email = form.cleaned_data['sender_email']
                smtp_setting.use_tls = form.cleaned_data['use_tls']
                smtp_setting.use_ssl = form.cleaned_data['use_ssl']
                smtp_setting.save()
                message = 'SMTP settings updated successfully.'
            else:
                # Add new SMTP setting
                SMTPSetting.objects.create(
                    host=form.cleaned_data['host'],
                    port=form.cleaned_data['port'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    sender_name=form.cleaned_data['sender_name'],
                    sender_email=form.cleaned_data['sender_email'],
                    use_tls=form.cleaned_data['use_tls'],
                    use_ssl=form.cleaned_data['use_ssl']
                )
                message = 'SMTP settings added successfully.'
            
            return JsonResponse({'status': True, 'message': message})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        smtp_id = request.GET.get('id')
        if smtp_id:
            smtp_setting = get_object_or_404(SMTPSetting, pk=smtp_id)
            form = SMTPForm(initial={
                'host': smtp_setting.host,
                'port': smtp_setting.port,
                'username': smtp_setting.username,
                'password': smtp_setting.password,
                'sender_email': smtp_setting.sender_email,
                'sender_name': smtp_setting.sender_name,
                'use_tls': smtp_setting.use_tls,
                'use_ssl': smtp_setting.use_ssl
            })
            form_title = 'Update SMTP Settings'
        else:
            form = SMTPForm()
            form_title = 'Add SMTP Settings'

        context = {
            'form': form,
            'form_title': form_title,
            'smtp_setting': smtp_setting if smtp_id else None,
            'button_text': 'Save SMTP',
            'clock_type': clock_type,
        }
        return render(request, 'smtp-add-update.html', context)
    

def test_smtp(request):
    if request.method == 'POST':
        smtp_id = request.POST.get('smtp_id')
        test_email = request.POST.get('test_email')
        smtp_setting = get_object_or_404(SMTPSetting, pk=smtp_id)
        sender = f"{smtp_setting.sender_name} <{smtp_setting.sender_email}>" if smtp_setting.sender_name else smtp_setting.username
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = test_email
        msg['Subject'] = 'SMTP Testing'
        message = f'This is a test email from {smtp_setting.host} SMTP'
        msg.attach(MIMEText(message))
        server = smtplib.SMTP(smtp_setting.host, smtp_setting.port)
        if smtp_setting.use_tls:
            server.starttls()
        server.login(smtp_setting.username, smtp_setting.password)
        server.sendmail(sender, test_email, msg.as_string())
        server.quit()
        return JsonResponse({'status': True, 'message': 'Test email sent successfully.'})



def delete_smtp(request, smtp_id):
    if request.method == 'POST':
        smtp = get_object_or_404(SMTPSetting, id=smtp_id)
        smtp.delete()
        msg = {"status": True, "message": "SMTP has been deleted successfully."}
        return JsonResponse(msg)
    return JsonResponse({"status": False, "message": "Invalid request."})


def settings_view(request):
    current_datetime = datetime.now()
    five_minutes_ahead = current_datetime + timedelta(minutes=5)
    min_datetime = five_minutes_ahead.strftime("%Y-%m-%dT%H:%M")
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    
    # Try to get the existing settings; if none exist, settings will be None
    settings = Settings.objects.first()

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)  # Pass the existing settings instance if it exists
        if form.is_valid():
            form.save()  # Save the form, which will update the existing settings or create new ones
            message = 'Settings saved successfully.'
            return JsonResponse({'status': True, 'message': message})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        form = SettingsForm(instance=settings)  # Pre-fill the form with the existing settings if they exist
        ctx = {
            "min_datetime": min_datetime,
            "form": form,
            "settings": settings,  # Pass the existing settings to the template
            "form_title": 'General Settings',
            'clock_type': clock_type,
        }
        return render(request, 'settings.html', ctx)


def campaign_view(request):
    campaigns = Campaign.objects.all()
    sent_campaigns = Campaign.objects.filter(sent=True)
    unsent_campaigns = Campaign.objects.filter(sent=False)
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    ctx = {
        "campaigns": campaigns,
        "sent_campaigns": sent_campaigns,
        "unsent_campaigns": unsent_campaigns,
        'clock_type': clock_type,
    }
    return render(request, 'campaigns.html', ctx)

def add_update_campaign(request):
    current_datetime = datetime.now()
    five_minutes_ahead = current_datetime + timedelta(minutes=5)
    min_datetime = five_minutes_ahead.strftime("%Y-%m-%dT%H:%M")
    segments = Segment.objects.all()
    smtps = SMTPSetting.objects.all()
    settings = Settings.objects.last()  # Fetch the latest settings
    clock_type = settings.clock_type if settings else 'Digital'
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign_id = request.POST.get('id')  # Get the ID from the POST data
            if campaign_id:
                campaign = get_object_or_404(Campaign, pk=campaign_id)
                campaign.campaign_name = form.cleaned_data['campaign_name']
                campaign.subject = form.cleaned_data['subject']
                campaign.content = form.cleaned_data['content']
                campaign.attachment_content = form.cleaned_data['attachment_content']
                campaign.filename = form.cleaned_data['filename']
                # campaign.attachment_type = form.cleaned_data['attachment_type']
                campaign.sender_type = form.cleaned_data['sender_type']
                campaign.segment = form.cleaned_data['segment']
                campaign.smtp = form.cleaned_data['smtp']
                campaign.save()
                message = 'Campaign updated successfully.'
            else:
                Campaign.objects.create(
                    campaign_name=form.cleaned_data['campaign_name'],
                    subject=form.cleaned_data['subject'],
                    content=form.cleaned_data['content'],
                    attachment_content=form.cleaned_data['attachment_content'],
                    filename=form.cleaned_data['filename'],
                    # attachment_type=form.cleaned_data['attachment_type'],
                    sender_type=form.cleaned_data['sender_type'],
                    segment=form.cleaned_data['segment'],
                    smtp=form.cleaned_data['smtp']
                )
                message = 'Campaign added successfully.'

            return JsonResponse({'status': True, 'message': message})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        campaign_id = request.GET.get('id')
        if campaign_id:
            campaign = get_object_or_404(Campaign, pk=campaign_id)
            form = CampaignForm(
                initial={
                    'campaign_name': campaign.campaign_name,
                    'subject': campaign.subject,
                    'content': campaign.content,
                    'attachment_content': campaign.attachment_content,
                    'filename': campaign.filename,
                    # 'attachment_type': campaign.attachment_type,
                    'sender_type': campaign.sender_type,
                    'segment': campaign.segment,
                    'smtp': campaign.smtp
                }
            )
            form_title = f'Update {campaign.campaign_name} Campaign'
        else:
            form = CampaignForm()
            form_title = 'Add Campaign'
        ctx = {
            "min_datetime": min_datetime,
            "segments": segments,
            "form": form,
            'campaign': campaign if campaign_id else None,
            "smtps": smtps,
            "form_title": form_title,
            'clock_type': clock_type,
        }
    return render(request, 'add-update-campaign.html', ctx)


def preview_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return JsonResponse({'content': campaign.content})


def send_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_number = int(data.get('contact_number', 100))

        # Get the segment contacts and limit to the specified number
        segment_contacts = campaign.segment.contacts.all()[:contact_number]

        for contact in segment_contacts:
            delay = random.randint(2, 15)
            campaign = Campaign.objects.get(id=campaign_id)
            contact = Contact.objects.get(id=contact.id)

            subject = campaign.subject
            smtp_setting = campaign.smtp
            setting_s = Settings.objects.last()
            message = replace_tags(campaign.content, contact, smtp_setting, setting_s)

            attachment_content = campaign.attachment_content
            filename = campaign.filename

            if attachment_content and filename:
                attachment_content = replace_tags(attachment_content, contact, smtp_setting, setting_s)

            connection = get_connection(
                host=smtp_setting.host,
                port=smtp_setting.port,
                username=smtp_setting.username,
                password=smtp_setting.password,
                use_tls=smtp_setting.use_tls,
                use_ssl=smtp_setting.use_ssl
            )
            namee, emailee = get_random_sender_info()
            sender_email = f"{namee} <{emailee}>" if campaign.sender_type == 'rotation' else f"{smtp_setting.sender_name} <{smtp_setting.sender_email}>"

            recipient_list = [contact.email]
            wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")  #by using configuration you can add path value.

            email = EmailMessage(subject, message, from_email=sender_email, to=recipient_list, connection=connection)
            email.content_subtype = 'html'  # Set the content type to HTML

            if attachment_content and filename:
                # Determine MIME type and handle content accordingly
                attachment_type = campaign.attachment_type.lower()
                if attachment_type == 'html':
                    mime_type = 'text/html'
                    attachment_content = attachment_content.encode('utf-8')  # Encode as bytes
                    filename = f"{filename}.html"
                elif attachment_type == 'pdf':
                    mime_type = 'application/pdf'
                    # Create a temporary file to save the PDF
                    with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        pdf_file_path = tmp_file.name
                        
                        try:
                            # Convert HTML snippet to PDF
                            pdfkit.from_string(attachment_content, pdf_file_path, configuration=wkhtml_path)
                            
                            # Read the PDF file as binary data
                            with open(pdf_file_path, 'rb') as file:
                                attachment_content = file.read()
                            
                            filename = f"{filename}.pdf"
                            
                        except Exception as e:
                            # Log error and return response
                            return JsonResponse({'status': False, 'message': f'Error generating PDF: {str(e)}'})
                        
                        # finally:
                        #     # Clean up: remove temporary PDF file
                        #     if os.path.exists(pdf_file_path):
                        #         os.remove(pdf_file_path)
                elif attachment_type == 'txt':
                    mime_type = 'text/plain'
                    attachment_content = attachment_content.encode('utf-8')  # Encode as bytes
                    filename = f"{filename}.txt"
                else:
                    mime_type = 'application/octet-stream'
                
                email.attach(filename, attachment_content, mime_type)

            # email.send(fail_silently=False)
            try:
                email.send(fail_silently=False)
                # Ensure the temporary file is removed after use
                os.remove(pdf_file_path)
                # SentContact.objects.create(contact=contact, campaign=campaign)
                # campaign.segment.contacts.remove(contact)
            except Exception as e:
                FailedContact.objects.create(contact=contact, campaign=campaign, error_message=str(e))
            campaign.status = "Attended"
            campaign.sent = True
            campaign.save()
            time.sleep(delay)

        return JsonResponse({'status': True, 'message': 'Campaign sent successfully.'})
    return JsonResponse({'status': False, 'message': 'Invalid request.'})


def Logout(request):
    logout(request)
    return redirect('login')
