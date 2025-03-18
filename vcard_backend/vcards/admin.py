# vcards/admin.py
from django.contrib import admin
from .models import Customer, VIPProfile, VCard

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone', 'company_name', 'customer_type')
    search_fields = ('user_name', 'phone', 'email', 'company_name')
    list_filter = ('customer_type',)

@admin.register(VIPProfile)
class VIPProfileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'custom_theme_color')

@admin.register(VCard)
class VCardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'portfolio_link')