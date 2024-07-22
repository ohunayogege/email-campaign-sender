from django import forms
from django_summernote.widgets import SummernoteWidget # type: ignore
from .models import Campaign, SMTPConfiguration, Subscriber


class SMTPConfigurationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = SMTPConfiguration
        fields = ['host', 'port', 'use_tls', 'username', 'password']

class UploadFileForm(forms.Form):
    file = forms.FileField()


class CampaignForm(forms.ModelForm):
    attachment_content = forms.CharField(widget=forms.Textarea, required=False, label="Attachment Content")
    sender_type = forms.ChoiceField(choices=Campaign.SENDER_CHOICES, required=True, label="Sender Type")
    # attachment_type = forms.ChoiceField(choices=[('html', 'HTML'), ('pdf', 'PDF')], required=True, label="Attachment Type")
    filename = forms.CharField(required=False, label="Attachment Filename")

    class Meta:
        model = Campaign
        fields = ['title', 'subject', 'content', 'attachment_content', 'filename', 'sender_type']
        widgets = {
            'content': SummernoteWidget(),
        }


class DomainSelectionForm(forms.Form):
    domain = forms.ChoiceField(choices=[], required=True)
    smtp = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(DomainSelectionForm, self).__init__(*args, **kwargs)
        unique_domains = Subscriber.objects.values_list('domain', flat=True).distinct()
        domain_choices = [('all', 'All Domains')] + [(domain, domain) for domain in unique_domains]
        smtp_choices = [(smtp.id, f"{smtp.host}:{smtp.port}") for smtp in SMTPConfiguration.objects.all()]
        self.fields['smtp'].choices = smtp_choices

        self.fields['domain'].choices = domain_choices
        self.fields['domain'].widget.attrs.update({'class': 'form-select form-control'})
        self.fields['smtp'].widget.attrs.update({'class': 'form-select form-control'})
