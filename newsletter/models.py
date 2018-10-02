from django.db import models
from phone_field import PhoneField


class NewsletterModel(models.Model):
    Name = models.CharField(max_length=100, default="", blank=False)
    News = models.CharField(max_length=1000, default="", blank=False)
    MobileNumber = PhoneField(default="", blank=False)
    MailID = models.EmailField(default="", blank=False)
