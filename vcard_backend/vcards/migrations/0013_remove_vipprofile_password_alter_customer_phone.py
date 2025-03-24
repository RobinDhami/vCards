# Generated by Django 5.1.7 on 2025-03-24 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcards', '0012_remove_vipprofile_company_logo_customer_company_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vipprofile',
            name='password',
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=20, unique=True, verbose_name='Phone Number'),
        ),
    ]
