from django.conf import settings
from django.urls import path
from vcards.views import *
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Create customer profile
    path('create/', create_customer, name='create_customer'),
    path('profile/', profile, name='profile'),
    path('admin/', admin.site.urls),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
