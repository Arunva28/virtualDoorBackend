from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from userinfo.models import BasicUserInfo
from datetime import datetime, timedelta, timezone, date
import datetime
from django.utils import timezone


class SecurityOffice(models.Model):
    Name = models.CharField(max_length=100, default="", blank=False)
    Unit = models.CharField(max_length=25, default="", blank=False)
    MobileNumber = PhoneField(default="", blank=False)
    VisitorMailID = models.EmailField(default="", blank=False)
    user = models.EmailField(default="", blank=False)
    Remarks = models.CharField(max_length=256, default="", blank=False)
    Date = models.DateField(default=datetime.date.today)
    Time = models.TimeField(default=datetime.time(1, 00))







