from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from vcards.views import *

urlpatterns = [
    path('rabin/', admin.site.urls),  # Admin URL
    path('', dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-customer/', create_customer, name='create_customer'),
    path('create-vcard/', create_vcard, name='create_vcard'),
    path('edit-customer/<int:customer_id>/', edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', delete_customer, name='delete_customer'),
    path('vcard/<int:customer_id>/', vcard_detail, name='vcard_detail'),
    path('customer/<int:customer_id>/', customer_profile, name='customer_profile'),
    path('download-vcard/<int:customer_id>/', download_vcard, name='download_vcard'),
    path('password-check/<int:customer_id>/', password_check, name='password_check'),
    path('customer/<int:customer_id>/analytics/', analytics, name='analytics'),
    path('tap-vcard/<int:customer_id>/', tap_vcard, name='tap_vcard'),
    path('save-vcard/<int:customer_id>/', save_vcard, name='save_vcard'),
    path('edit-vip-profile/<int:customer_id>/', edit_vip_profile, name='edit_vip_profile'),
    # School & Student Management URLs
    path('school_dashboard/', school_dashboard, name='school_dashboard'),
    path('create_school/', create_school, name='create_school'),
    path('edit_school/<int:school_id>/', edit_school, name='edit_school'),
    path('delete_school/<int:school_id>/', delete_school, name='delete_school'),
    
    # View Students under a School
    path('view_students/<int:school_id>/', view_students, name='view_students'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)