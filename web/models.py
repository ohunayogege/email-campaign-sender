from django.db import models
import string
import random

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class URLShortener(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, default=generate_short_code)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class SMTPConfiguration(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    use_tls = models.BooleanField(default=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.host}:{self.port}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class MessageLog(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} to {self.subscriber.email}'


class Campaign(models.Model):
    SENDER_CHOICES = [
        ('rotate', 'Rotate Sender'),
        ('default', 'Default Sender')
    ]
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    attachment_content = models.TextField(blank=True, null=True)  # New field for attachment content
    filename = models.CharField(max_length=255, default='', blank=True)
    attachment_type = models.CharField(max_length=255, default='html', blank=True)
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title