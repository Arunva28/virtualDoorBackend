# Generated by Django 2.0.6 on 2018-09-30 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0006_auto_20181001_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society_creategroupmodel',
            name='nameofgroup',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
