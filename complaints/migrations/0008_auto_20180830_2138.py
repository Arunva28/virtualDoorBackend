# Generated by Django 2.1 on 2018-08-30 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0007_auto_20180830_2135'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TicketDescription',
        ),
        migrations.DeleteModel(
            name='TicketList',
        ),
        migrations.DeleteModel(
            name='TicketsName',
        ),
    ]
