from django.db import models
from decimal import Decimal


# Create your models here.
class TicketDescription(models.Model):
    Section = models.CharField(max_length=255)
    Description = models.CharField(max_length=1000)
    IssueResolved = models.BooleanField(default=False,blank=True)
    Feedback = models.CharField(max_length=255,blank=True)
    Created = models.DateTimeField(auto_now=True)
    Modified = models.DateTimeField(auto_now=True)
    UserID = models.CharField(max_length=100, default="")
    TicketID = models.DecimalField(max_digits=20, decimal_places=0, default=Decimal('0'))
    BuildingName = models.CharField(max_length=100, default="")


class TicketList(models.Model):
    WaterIssues = models.CharField(max_length=255)
    ElectricityIssues = models.CharField(max_length=1000)
    BuildingIssues = models.BooleanField(default=False)
    SecurityIssues = models.CharField(max_length=255)
    BookingIssues = models.DateTimeField(auto_now=True)
    Others = models.DateTimeField(auto_now=True)


class TicketsName(models.Model):
    TypeofIssue = models.CharField(max_length=255)
