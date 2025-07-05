from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skill, blank=True)
    views = models.IntegerField(default=0)

    # Social Media Links
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    figma = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    upwork = models.URLField(blank=True, null=True)
    other = models.URLField(blank=True, null=True)




    about = models.TextField(blank=True)
    education = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='covers/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
