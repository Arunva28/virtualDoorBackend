# Generated by Django 2.0.5 on 2018-05-26 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securityoffice',
            name='user',
        ),
        migrations.AlterField(
            model_name='securityoffice',
            name='Reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
