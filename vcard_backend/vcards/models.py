from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File


class VCard(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(default='mail@gmail.com')  # Provide a default value
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    USER_TYPES = [
        ('normal', 'Normal'),
        ('vip', 'VIP'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(default='default@example.com')  # Provide a default value to prevent null values
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)  
    bio = models.TextField(blank=True, null=True)  # blank=True, null=True
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    # VIP exclusive fields
    portfolio_link = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generate_qr_code(self):
        qr_data = f"https://tap2solve.com/profile/{self.id}/"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        self.qr_code.save(f'{self.first_name}_{self.id}_qr.png', File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"
