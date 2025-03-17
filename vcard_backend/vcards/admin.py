# vcards/admin.py

from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone', 'email', 'customer_type', 'profile_photo')
    search_fields = ('user_name', 'email', 'phone')
