# Generated by Django 2.1 on 2018-08-30 19:43

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('complaints', '0008_auto_20180830_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Section', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=1000)),
                ('IssueResolved', models.BooleanField(default=False)),
                ('Feedback', models.CharField(max_length=255)),
                ('Created', models.DateTimeField(auto_now=True)),
                ('Modified', models.DateTimeField(auto_now=True)),
                ('UserID', models.CharField(default='', max_length=100)),
                ('TicketID', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=20)),
                ('BuildingName', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TicketList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WaterIssues', models.CharField(max_length=255)),
                ('ElectricityIssues', models.CharField(max_length=1000)),
                ('BuildingIssues', models.BooleanField(default=False)),
                ('SecurityIssues', models.CharField(max_length=255)),
                ('BookingIssues', models.DateTimeField(auto_now=True)),
                ('Others', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TicketsName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TypeofIssue', models.CharField(max_length=255)),
            ],
        ),
    ]
