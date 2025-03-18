from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from vcards.views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-customer/', create_customer, name='create_customer'),
    path('create-vcard/', create_vcard, name='create_vcard'),
    path('edit-customer/<int:customer_id>/', edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', delete_customer, name='delete_customer'),
    path('vcard/<int:customer_id>/', vcard_detail, name='vcard_detail'),
    path('customer/<int:customer_id>/', customer_profile, name='customer_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)