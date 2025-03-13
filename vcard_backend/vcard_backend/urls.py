from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from django.contrib import admin
from django.urls import path, include  # Ensure include is imported
from vcards.views import home  # Import the home view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vcards.urls')),  # Include the vcards app URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
