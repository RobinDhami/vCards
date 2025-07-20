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
    path('dashboard/create/', add_user, name='add_user'),
    path('dashboard/college_details/<int:college_id>/', college_details, name='college_details'),
    path('dashboard/edit_college/<int:college_id>/', edit_college, name='edit_college'),
    path('dashboard/add_college/', add_college, name='add_college'),
    path('dashboard/delete_college/<int:college_id>/', delete_college, name='delete_college'),
    path('dashboard/edit-auth/<int:student_id>/', edit_student_auth, name='edit_student_auth'),
    path('dashboard/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('bulk-upload/', bulk_upload, name='bulk_upload'),
    path('dashboard/college/<int:college_id>/add_student/', add_student_to_college, name='add_student_to_college'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)