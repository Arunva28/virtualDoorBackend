from django.db import models
from phone_field import PhoneField


class Society_creategroupmodel(models.Model):
    nameofgroup = models.CharField(max_length=100, default="",unique=True, blank=False)
    description = models.CharField(max_length=100, default="", blank=False)
    mailid = models.EmailField(default="", blank=False)
    adminofgroup = models.BooleanField(default=True)
    groupaprrovedbybuildingadmin = models.BooleanField(default=False)
    restrictedtomybuilding = models.BooleanField(default=True)


class Society_memberaddmodel(models.Model):
    group = models.CharField(max_length=100, default="", blank=False)
    mailid = models.EmailField(default="", blank=False)
    chat = models.CharField(max_length=200, default="New request", blank=False)
    approvedbygroupadmin = models.BooleanField(default=False)
