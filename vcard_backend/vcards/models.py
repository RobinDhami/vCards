from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Existing Skill model (keep as is)
class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Improved Student model with all new fields
class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Use hashed password if possible

    # New fields
    address = models.CharField(max_length=255, blank=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    education_completed = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    about_me = models.TextField(blank=True)

    # Media fields
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Skills
    skills = models.ManyToManyField(Skill, blank=True)

    # Social links
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    figma = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    upwork = models.URLField(blank=True, null=True)
    other = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# New Project model
class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.student.name})"



    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
