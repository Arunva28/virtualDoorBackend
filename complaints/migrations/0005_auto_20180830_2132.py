# Generated by Django 2.1 on 2018-08-30 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_auto_20180830_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketdescription',
            name='BuildingName',
        ),
        migrations.RemoveField(
            model_name='ticketdescription',
            name='TicketID',
        ),
    ]
