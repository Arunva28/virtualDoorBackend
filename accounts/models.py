from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
import datetime
# Create your models here.

class Description(models.Model):
    Fields = models.CharField(max_length=100, default="")


class AccountsModel(models.Model):
    Type = models.CharField(max_length=100, default="")
    Amount = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.0000'))
    IsExpense = models.BooleanField(default=False)
    buildingName = models.CharField(max_length=255, default="")
    unitNo = models.CharField(max_length=255, default="")
    houseNo = models.CharField(max_length=255, default="")
    Date = models.DateField(default=datetime.date.today)
    user = models.EmailField(default="")
    expenseApproved = models.BooleanField(default=False)

