from django.contrib import admin
from .models import College, StudentProfile, ClientProfile, Skill

admin.site.register(College)
admin.site.register(StudentProfile)
admin.site.register(ClientProfile)
admin.site.register(Skill)