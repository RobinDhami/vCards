from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from vcards.views import *

urlpatterns = [
    path('',home,name='home'),
    path('profile/<int:student_id>/',profile,name='profile'),
    path('admin/', admin.site.urls),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/create/', create_student, name='create_student'),
    path('dashboard/edit-auth/<int:student_id>/', edit_student_auth, name='edit_student_auth'),
    path('dashboard/edit/<int:student_id>/', edit_student, name='edit_student'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)