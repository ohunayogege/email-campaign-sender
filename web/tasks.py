from time import sleep
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import get_connection, EmailMessage
from web.utils import get_random_sender_info, send_email
from .models import Campaign, Contact, FailedContact, SentContact
from django.conf import settings

@shared_task
def send_campaign_email_task(campaign_id, contact_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        contact = Contact.objects.get(id=contact_id)

        subject = campaign.subject
        message = campaign.content.replace("[[Email]]", contact.email)
        smtp_setting = campaign.smtp_setting

        connection = get_connection(
            host=smtp_setting.host,
            port=smtp_setting.port,
            username=smtp_setting.username,
            password=smtp_setting.password,
            use_tls=smtp_setting.use_tls,
            use_ssl=smtp_setting.use_ssl
        )
        print(get_random_sender_info())

        if campaign.sender_type == 'rotation':
            sender_email = get_random_sender_info()
        else:
            sender_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [contact.email]

        email = EmailMessage(subject, message, from_email=sender_email, to=recipient_list, connection=connection)
        email.send(fail_silently=False)
        print(email)

        SentContact.objects.create(contact=contact, campaign=campaign)
        campaign.segment.contacts.remove(contact)

    except Exception as e:
        FailedContact.objects.create(contact=contact, campaign=campaign, error_message=str(e))
        # Handle logging of the error if necessary

    # Introduce a delay to avoid spamming
    sleep(2)  # 2 seconds delay between each email; adjust as needed
