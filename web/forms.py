from django import forms
from .models import Campaign, Contact, Segment, ContactList, Settings

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'segment', 'is_active']

class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ['name']

class ContactListForm(forms.ModelForm):
    class Meta:
        model = ContactList
        fields = ['name', 'contacts', 'subscription_management']


class SMTPForm(forms.Form):
    host = forms.CharField(max_length=255)
    port = forms.IntegerField()
    sender_name = forms.CharField(max_length=255)
    sender_email = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    use_tls = forms.BooleanField(required=False)
    use_ssl = forms.BooleanField(required=False)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['email_tag', 'name_tag', 'time_tag', 'date_tag', 'clock_type']

class CampaignForm(forms.ModelForm):
    attachment_content = forms.CharField(widget=forms.Textarea, required=False, label="Attachment Content")
    sender_type = forms.ChoiceField(choices=Campaign.SENDER_CHOICES, required=True, label="Sender Type")
    # attachment_type = forms.ChoiceField(choices=[('html', 'HTML'), ('pdf', 'PDF')], required=True, label="Attachment Type")
    filename = forms.CharField(required=False, label="Attachment Filename")

    class Meta:
        model = Campaign
        fields = ['campaign_name', 'subject', 'content', 'attachment_content', 'segment', 'smtp', 'filename', 'sender_type']
