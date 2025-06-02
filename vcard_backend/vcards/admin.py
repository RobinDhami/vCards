from django.contrib import admin
from .models import Student, Skill

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    filter_horizontal = ('skills',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Skill)
