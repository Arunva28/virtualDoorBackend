# Generated by Django 2.0.6 on 2018-10-02 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20181002_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendormodel',
            old_name='Designation',
            new_name='Merchant',
        ),
    ]