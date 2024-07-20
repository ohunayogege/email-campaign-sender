from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import tempfile
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
import smtplib
from django.contrib import messages
from web.forms import CampaignForm, DomainSelectionForm, SMTPConfigurationForm, UploadFileForm
from web.models import Campaign, MessageLog, SMTPConfiguration, Subscriber, URLShortener
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
import re
from web.utils import decrypt_url, encrypt_url, generate_short_code, get_random_sender_info, replace_links_with_short_urls, shorten_url

def dashboard(request):
    campaigns = Campaign.objects.all()
    subscribers = Subscriber.objects.all()
    messageLogs = MessageLog.objects.all()
    ctx = {
        "campaigns": campaigns,
        "subscribers": subscribers,
        "messageLogs": messageLogs,
    }
    return render(request, 'dashboard.html', ctx)


def add_smtp_configuration(request):
    if request.method == 'POST':
        form = SMTPConfigurationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('smtp_list')
    else:
        form = SMTPConfigurationForm()
    return render(request, 'add_smtp_configuration.html', {'form': form})

def delete_smtp_configuration(request, smtp_id):
    smtp_config = get_object_or_404(SMTPConfiguration, pk=smtp_id)
    if request.method == 'POST':
        smtp_config.delete()
        return redirect('smtp_list')
    return render(request, 'delete_smtp_configuration.html', {'smtp_config': smtp_config})


def smtp_list(request):
    smtp_configs = SMTPConfiguration.objects.all()
    return render(request, 'smtp_list.html', {'smtp_configs': smtp_configs})


def test_smtp_configuration(request):
    if request.method == 'POST':
        config_id = request.POST.get('config_id')
        recipient_email = request.POST.get('recipient_email')
        smtp_config = get_object_or_404(SMTPConfiguration, pk=config_id)

        try:
            server = smtplib.SMTP(smtp_config.host, smtp_config.port)
            if smtp_config.use_tls:
                server.starttls()
            server.login(smtp_config.username, smtp_config.password)
            message = "Subject: Test Email\n\nThis is a test email."
            server.sendmail(smtp_config.username, recipient_email, message)
            server.quit()
            messages.success(request, 'Test email sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send test email: {e}')

        return redirect('smtp_list')


def import_subscribers(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith('.txt'):
                messages.error(request, 'File is not a .txt file')
                return redirect('import_subscribers')

            subscribers = []
            total_lines = sum(1 for line in file)
            file.seek(0)  # Reset file pointer to beginning
            processed_lines = 0
            channel_layer = get_channel_layer()
            for line in file:
                email = line.decode('utf-8').strip()
                if not email:
                    continue
                name = email.split('@')[0].replace('.', ' ').title()
                domain = email.split('@')[1]
                subscribers.append(Subscriber(email=email, name=name, domain=domain))
                processed_lines += 1
                progress = int((processed_lines / total_lines) * 100)
                async_to_sync(channel_layer.group_send)(
                    'import_progress',
                    {
                        'type': 'send_progress',
                        'progress': progress
                    }
                )

            try:
                Subscriber.objects.bulk_create(subscribers)
                messages.success(request, 'Subscribers imported successfully!')
            except Exception as e:
                messages.error(request, f'Error importing subscribers: {e}')

            return redirect('subscriber_list')
    else:
        form = UploadFileForm()
    return render(request, 'import_subscribers.html', {'form': form})


def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'subscriber_list.html', {'subscribers': subscribers})

def delete_all_subscribers(request):
    if request.method == 'POST':
        Subscriber.objects.all().delete()
        messages.success(request, 'All subscribers have been deleted.')
        return redirect('subscriber_list')
    subscribers = Subscriber.objects.all()
    return render(request, 'confirm_delete_all.html', {'subscribers': subscribers})

def message_log_list(request):
    logs = MessageLog.objects.all()
    return render(request, 'message_log_list.html', {'logs': logs})


def campaign_list(request):
    campaigns = Campaign.objects.all()
    domain_form = DomainSelectionForm()
    return render(request, 'campaign_list.html', {'campaigns': campaigns, 'domain_form': domain_form})


def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign created successfully!')
            return redirect('campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'campaign_form.html', {'form': form})

def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully!')
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaign_form.html', {'form': form})

def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted successfully!')
        return redirect('campaign_list')
    return render(request, 'confirm_delete_campaign.html', {'campaign': campaign})

def get_smtp_config(campaign):
    if campaign.sender_type == 'random':
        smtp_configurations = SMTPConfiguration.objects.all()
        return random.choice(smtp_configurations)
    elif campaign.sender_type == 'specific':
        return campaign.specific_sender
    else:
        return SMTPConfiguration.objects.first()  # Assuming the first one is the default

def send_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        form = DomainSelectionForm(request.POST)

        if form.is_valid():
            domain = form.cleaned_data['domain']
            smtp_id = form.cleaned_data['smtp']

            if domain == 'all':
                subscribers = Subscriber.objects.all()
            else:
                subscribers = Subscriber.objects.filter(domain=domain)

            smtp_config = get_object_or_404(SMTPConfiguration, pk=smtp_id)
            if not smtp_config:
                messages.error(request, 'No SMTP configuration found.')
                return redirect('campaign_list')

            try:
                server = smtplib.SMTP(smtp_config.host, smtp_config.port)
                if smtp_config.use_tls:
                    server.starttls()
                server.login(smtp_config.username, smtp_config.password)

                attachment_content = campaign.attachment_content
                attachment_path = None
                if attachment_content:
                    # Replace links with Bitly short URLs in attachment content
                    soup2 = BeautifulSoup(attachment_content, 'html.parser')
                    for a2 in soup2.find_all('a', href=True):
                        original_url2 = a2['href']
                        short_url2 = shorten_url(original_url2)
                        a2['href'] = short_url2

                    # Save the modified attachment content to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as temp_file:
                        temp_file.write(str(soup2))
                        attachment_path = temp_file.name

                for subscriber in subscribers:
                    if campaign.sender_type == 'rotate':
                        print("Rotating...")
                        sender_name, sender_email = get_random_sender_info()
                    else:
                        sender_name = smtp_config.sender_name
                        sender_email = smtp_config.sender_email

                    if not sender_name or not sender_email:
                        messages.error(request, 'No sender information found.')
                        return redirect('campaign_list')

                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = campaign.subject
                    msg['From'] = f'{sender_name} <{sender_email}>'
                    msg['To'] = subscriber.email

                    # Parse the HTML content and replace links with Bitly short URLs
                    soup = BeautifulSoup(campaign.content, 'html.parser')
                    for a in soup.find_all('a', href=True):
                        original_url = a['href']
                        short_url = shorten_url(original_url)
                        a['href'] = short_url

                    html_content = str(soup)

                    part = MIMEText(html_content, 'html')
                    msg.attach(part)

                    # Attach the modified file if it exists
                    if attachment_path:
                        with open(attachment_path, 'rb') as file:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename=attachment.html',
                            )
                            msg.attach(part)

                    server.sendmail(sender_email, subscriber.email, msg.as_string())
                    MessageLog.objects.create(subscriber=subscriber, subject=campaign.subject, content=campaign.content)

                server.quit()
                messages.success(request, 'Campaign sent successfully!')

                # Clean up the temporary file
                if attachment_path:
                    os.remove(attachment_path)

            except Exception as e:
                messages.error(request, f'Failed to send campaign: {e}')
        else:
            messages.error(request, 'Invalid domain or SMTP selected.')

    return redirect('campaign_list')


def redirect_order(request, token):
    try:
        original_url = token
        return redirect(original_url)
    except Exception:
        return HttpResponseBadRequest("Invalid token")


def redirect_short_url(request, short_code):
    url_entry = get_object_or_404(URLShortener, short_code=short_code)
    return redirect(url_entry.original_url)

def create_short_url(original_url):
    short_url, created = URLShortener.objects.get_or_create(original_url=original_url)
    if created:
        short_url.short_code = generate_short_code()
        short_url.save()
    return short_url.short_code
