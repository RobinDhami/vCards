# Generated by Django 5.1.7 on 2025-04-12 05:21

import django.db.models.deletion
import vcards.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='Phone Number')),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('instagram', models.CharField(blank=True, max_length=255, null=True, verbose_name='Instagram Handle')),
                ('facebook', models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook Profile')),
                ('twitter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Twitter Handle')),
                ('linkedin', models.CharField(blank=True, max_length=255, null=True, verbose_name='LinkedIn Profile')),
                ('youtube', models.CharField(blank=True, max_length=255, null=True, verbose_name='YouTube Channel')),
                ('tiktok', models.CharField(blank=True, max_length=255, null=True, verbose_name='TikTok Profile')),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True, verbose_name='WhatsApp Number')),
                ('personal_website', models.URLField(blank=True, null=True, verbose_name='Personal Website')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('nfc_taps', models.IntegerField(default=0)),
                ('vcard_views', models.IntegerField(default=0)),
                ('vcard_saves', models.IntegerField(default=0)),
                ('customer_type', models.CharField(choices=[('general', 'General'), ('vip', 'VIP')], default='general', max_length=10, verbose_name='Customer Type')),
                ('profile_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='profile_photos/', verbose_name='Profile Photo')),
                ('cover_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='cover_photos/', verbose_name='Cover Photo')),
                ('company_logo', models.ImageField(blank=True, max_length=255, null=True, upload_to='company_logos/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Customer Profile',
                'verbose_name_plural': 'Customer Profiles',
                'ordering': ['user_name'],
            },
        ),
        migrations.CreateModel(
            name='VCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to=vcards.models.qr_code_path)),
                ('portfolio_link', models.URLField()),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vcards.customer')),
            ],
        ),
        migrations.CreateModel(
            name='VIPProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_theme_color', models.CharField(blank=True, max_length=7, null=True, verbose_name='Theme Color (Hex)')),
                ('custom_banner_image', models.ImageField(blank=True, null=True, upload_to=vcards.models.vip_banner_path, verbose_name='Banner Image')),
                ('vcard_views', models.IntegerField(default=0)),
                ('vcard_taps', models.IntegerField(default=0)),
                ('vcard_saves', models.IntegerField(default=0)),
                ('primary_color', models.CharField(default='#ffffff', max_length=7)),
                ('custom_background', models.CharField(blank=True, max_length=7, null=True)),
                ('secondary_color', models.CharField(blank=True, max_length=7, null=True)),
                ('accent_color', models.CharField(blank=True, max_length=7, null=True)),
                ('custom_font', models.CharField(blank=True, max_length=100, null=True)),
                ('custom_stylesheet', models.TextField(blank=True, null=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vip_profile', to='vcards.customer')),
            ],
        ),
    ]
