from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Customer, VIPProfile, VCard

# Customize UserAdmin to manage the User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # Use the default fieldsets (do not duplicate the password field)
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

# Unregister the default UserAdmin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize the CustomerAdmin to display profile and customer data
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'user_name', 'phone', 'company_name', 'email', 'customer_type', 'profile_photo_preview'
    )
    search_fields = ('user_name', 'phone', 'email', 'company_name')
    list_filter = ('customer_type',)
    ordering = ('user_name',)
    
    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return f'<img src="{obj.profile_photo.url}" style="max-width: 50px; max-height: 50px;" />'
        return 'No photo'
    profile_photo_preview.allow_tags = True
    profile_photo_preview.short_description = 'Profile Photo'

# VIPProfile Admin
@admin.register(VIPProfile)
class VIPProfileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'custom_theme_color')
    search_fields = ('customer__user_name', 'customer__email')
    list_filter = ('custom_theme_color',)

# VCard Admin
@admin.register(VCard)
class VCardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'portfolio_link')
    search_fields = ('customer__user_name', 'portfolio_link')
    list_filter = ('customer__customer_type',)
