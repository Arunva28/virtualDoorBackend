from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
import datetime



# Create your models here.
class BasicUserInfo(AbstractUser):
    email = models.EmailField(primary_key=True, unique=True, db_index=True)


class UserInfo(models.Model):
    user = models.OneToOneField(BasicUserInfo, on_delete=models.CASCADE)
    phoneNo = PhoneField(default="")
    unitNo = models.CharField(max_length=255, default="")
    buildingName = models.CharField(max_length=255, default="")
    isAdmin = models.BooleanField(default=False)


class ForgotPassword(models.Model):
    user_email = models.OneToOneField(BasicUserInfo, on_delete=models.CASCADE)
    otp = models.BigIntegerField(default="")
    date_time = models.DateTimeField(default=datetime.date.today)

