from django.db import models
from django.contrib.auth.hashers import make_password

# -------------------------
# Skill model
# -------------------------
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -------------------------
# College model
# -------------------------
class College(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


# -------------------------
# Abstract Base Profile
# -------------------------
class BaseProfile(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # store hashed version

    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)

    skills = models.ManyToManyField(Skill, blank=True)

    # Show/hide toggles
    show_portfolio = models.BooleanField(default=True)
    show_contact_card = models.BooleanField(default=True)

    # Social media links
    facebook = models.URLField(blank=True, null=True)
    messenger= models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=20,null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    figma = models.URLField(blank=True, null=True)
    upwork = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Analytics
    views = models.PositiveIntegerField(default=0)
    contact_clicks = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# -------------------------
# Student Profile (College)
# -------------------------
class StudentProfile(BaseProfile):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.name} - {self.college.name}"


# -------------------------
# Client Profile (Normal User)
# -------------------------
class ClientProfile(BaseProfile):
    company_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name