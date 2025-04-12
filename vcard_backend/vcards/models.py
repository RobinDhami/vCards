from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
import qrcode

# Customer Types Enum
class CustomerType(models.TextChoices):
    GENERAL = 'general', 'General'
    VIP = 'vip', 'VIP'

# Dynamic upload paths
def profile_photo_path(instance, filename):
    return f"profile_photos/{instance.user.id}/{filename}"

def cover_photo_path(instance, filename):
    return f"cover_photos/{instance.user.id}/{filename}"

def vip_banner_path(instance, filename):
    return f"vip_banners/{instance.customer.user.id}/{filename}"

def qr_code_path(instance, filename):
    return f"qr_codes/{instance.customer.user.id}/{filename}"

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    user_name = models.CharField(max_length=255, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number", unique=True)
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    email = models.EmailField(verbose_name="Email Address")
    instagram = models.CharField(max_length=255, blank=True, null=True, verbose_name="Instagram Handle")
    facebook = models.CharField(max_length=255, blank=True, null=True, verbose_name="Facebook Profile")
    twitter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Twitter Handle")
    linkedin = models.CharField(max_length=255, blank=True, null=True, verbose_name="LinkedIn Profile")
    youtube = models.CharField(max_length=255, blank=True, null=True, verbose_name="YouTube Channel")
    tiktok = models.CharField(max_length=255, blank=True, null=True, verbose_name="TikTok Profile")
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="WhatsApp Number")
    personal_website = models.URLField(blank=True, null=True, verbose_name="Personal Website")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    nfc_taps = models.IntegerField(default=0)  # Track NFC card taps
    vcard_views = models.IntegerField(default=0)  # Track vCard views
    vcard_saves = models.IntegerField(default=0)  # Track vCard saves
    customer_type = models.CharField(
        max_length=10,
        choices=CustomerType.choices,
        default=CustomerType.GENERAL,
        verbose_name="Customer Type"
    )
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="Profile Photo", max_length=255)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True, verbose_name="Cover Photo", max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', max_length=255, blank=True, null=True)

    @property
    def is_vip(self):
        return self.customer_type == CustomerType.VIP

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
        ordering = ['user_name']

# VIP Profile Model (Extra Customization for VIPs)
class VIPProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='vip_profile')
    custom_theme_color = models.CharField(max_length=7, blank=True, null=True, verbose_name="Theme Color (Hex)")
    custom_banner_image = models.ImageField(upload_to=vip_banner_path, blank=True, null=True, verbose_name="Banner Image")
    vcard_views = models.IntegerField(default=0)
    vcard_taps = models.IntegerField(default=0)
    vcard_saves = models.IntegerField(default=0)
    primary_color = models.CharField(max_length=7, default="#ffffff")  # Hex color code
    custom_background = models.CharField(max_length=7, blank=True, null=True)  # Hex color or URL for background

    # Other branding options
    secondary_color = models.CharField(max_length=7, blank=True, null=True)  # For secondary branding color
    accent_color = models.CharField(max_length=7, blank=True, null=True)  # For accent color
    custom_font = models.CharField(max_length=100, blank=True, null=True)  # For custom fonts

    # Additional features for VIP (optional)
    custom_stylesheet = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"VIP Profile for {self.customer.user_name}"

# VCard Model
class VCard(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to=qr_code_path, null=True, blank=True)
    portfolio_link = models.URLField()

    def save(self, *args, **kwargs):
        # Check if portfolio_link has changed or QR code doesn't exist
        if not self.pk or not self.qr_code:
            self.generate_qr_code()
        else:
            old_vcard = VCard.objects.get(pk=self.pk)
            if old_vcard.portfolio_link != self.portfolio_link:
                self.generate_qr_code()
        super(VCard, self).save(*args, **kwargs)

    def generate_qr_code(self):
        qr = qrcode.make(self.portfolio_link)
        qr_img = BytesIO()
        qr.save(qr_img)
        qr_img.seek(0)
        qr_filename = f"{self.customer.user_name}_qr.png"
        self.qr_code.save(qr_filename, File(qr_img), save=False)

    def __str__(self):
        return f"vCard for {self.customer.user_name}"


# Dynamic Upload Paths
def profile_photo_path(instance, filename):
    return f"students/profile_photos/{instance.user.id}/{filename}"

def qr_code_path(instance, filename):
    return f"students/qr_codes/{instance.user.id}/{filename}"

