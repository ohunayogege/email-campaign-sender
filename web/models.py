from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.forms import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.user_id


class Segment(models.Model):
    name = models.CharField(max_length=100, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default=None)
    email = models.EmailField(max_length=100, default='')
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='contacts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class ContactList(models.Model):
    name = models.CharField(max_length=100, default=None)
    contacts = models.ManyToManyField(Contact, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_management = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SMTPSetting(models.Model):
    host = models.CharField(max_length=255, default='')
    port = models.IntegerField(default="")
    username = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    use_tls = models.BooleanField(default=False)
    use_ssl = models.BooleanField(default=False)
    sender_name = models.CharField(max_length=255, blank=True, null=True)
    sender_email = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.host}:{self.port}"

    class Meta:
        verbose_name = 'SMTP Setting'
        verbose_name_plural = 'SMTP Settings'


class Settings(models.Model):
    email_tag = models.CharField(max_length=255, default='[[Email]]')
    name_tag = models.CharField(max_length=255, default='[[Name]]')
    time_tag = models.CharField(max_length=255, default='[[Time]]')
    date_tag = models.CharField(max_length=255, default='[[Date]]')
    
    CLOCK_TYPE_CHOICES = [
        ('Analog', 'Analog'),
        ('Digital', 'Digital'),
    ]
    clock_type = models.CharField(
        max_length=7,
        choices=CLOCK_TYPE_CHOICES,
        default='Digital',
    )
    

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            raise ValidationError('Only one Settings instance is allowed.')
        return super(Settings, self).save(*args, **kwargs)

    def __str__(self):
        return f"Settings (Clock Type: {self.clock_type})"
    
    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=255, default="")
    SENDER_CHOICES = [
        ('rotate', 'Rotate Sender'),
        ('default', 'Default Sender')
    ]
    subject = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    attachment_content = models.TextField(blank=True, null=True)  # New field for attachment content
    filename = models.CharField(max_length=255, default='', blank=True)
    attachment_type = models.CharField(max_length=255, default='html', blank=True)
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES, default='default')
    status = models.CharField(max_length=255, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='campaigns', blank=True, null=True)
    sent = models.BooleanField(default=False)
    smtp = models.ForeignKey(SMTPSetting, on_delete=models.CASCADE, related_name='smtp', blank=True, null=True)

    def __str__(self):
        return self.campaign_name

class SentContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.contact.email

class FailedContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    failed_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.contact.email