# Generated by Django 5.1.7 on 2025-03-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcards', '0006_vipprofile_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipprofile',
            name='vcard_saves',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vipprofile',
            name='vcard_taps',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vipprofile',
            name='vcard_views',
            field=models.IntegerField(default=0),
        ),
    ]
