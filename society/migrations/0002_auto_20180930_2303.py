# Generated by Django 2.0.6 on 2018-09-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society_creategroupmodel',
            name='mailid',
            field=models.EmailField(default='', max_length=254),
        ),
    ]