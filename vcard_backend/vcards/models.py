from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")  # This will display "User" in the admin
    user_name = models.CharField(max_length=255, verbose_name="Full Name")  # Renamed for more readable display
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    email = models.EmailField(verbose_name="Email Address")
    instagram = models.CharField(max_length=255, blank=True, null=True, verbose_name="Instagram Handle")
    facebook = models.CharField(max_length=255, blank=True, null=True, verbose_name="Facebook Profile")
    twitter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Twitter Handle")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    customer_type = models.CharField(
        max_length=10,
        choices=[('general', 'General'), ('vip', 'VIP')],
        verbose_name="Customer Type"
    )
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="Profile Photo")  # Optional field

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Customer Profile"  # This will be used in the admin interface for this model
        verbose_name_plural = "Customer Profiles"  # Plural form for the admin



import qrcode
from django.db import models
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings

class VCard(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)  # To store the generated QR code image
    portfolio_link = models.URLField()  # URL that leads to the customer's online portfolio (generated after profile creation)
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super(VCard, self).save(*args, **kwargs)
    
    def generate_qr_code(self):
        qr = qrcode.make(self.portfolio_link)
        qr_img = BytesIO()
        qr.save(qr_img)
        qr_img.seek(0)
        self.qr_code.save(f"{self.customer.user_name}_qr.png", File(qr_img), save=False)

    def __str__(self):
        return f"vCard for {self.customer.user_name}"
