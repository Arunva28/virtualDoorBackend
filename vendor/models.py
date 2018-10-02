from django.db import models
from phone_field import PhoneField


class VendorModel(models.Model):
    Name = models.CharField(max_length=100, default="", blank=False)
    Merchant = models.CharField(max_length=25, default="", blank=False)
    MobileNumber = PhoneField(default="", blank=False)
    MailID = models.EmailField(default="", blank=False)
