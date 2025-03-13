# admin.py
from django.contrib import admin
from .models import VCard, UserProfile

class VCardAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'qr_code')
    search_fields = ('first_name', 'last_name', 'phone', 'email')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'user_type', 'portfolio_link', 'linkedin', 'twitter', 'qr_code')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'user_type')
    list_filter = ('user_type',)
    readonly_fields = ('qr_code',)

admin.site.register(VCard, VCardAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
