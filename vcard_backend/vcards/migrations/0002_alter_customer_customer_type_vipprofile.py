# Generated by Django 5.1.7 on 2025-03-18 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_type',
            field=models.CharField(choices=[('general', 'General'), ('vip', 'VIP')], default='general', max_length=10, verbose_name='Customer Type'),
        ),
        migrations.CreateModel(
            name='VIPProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_theme_color', models.CharField(blank=True, max_length=7, null=True, verbose_name='Theme Color (Hex)')),
                ('custom_banner_image', models.ImageField(blank=True, null=True, upload_to='vip_banners/', verbose_name='Banner Image')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vip_profile', to='vcards.customer')),
            ],
        ),
    ]
