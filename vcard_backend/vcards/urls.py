# vcards/urls.py
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from . import views  # Import views from the 'vcards' app
from .views import VCardListCreateView, VCardDetailView, UserProfileListCreateView, UserProfileDetailView
from django.conf.urls.static import static

def home(request):
    return HttpResponse("Welcome to the TapToSolve API!")

urlpatterns = [
    path('', home, name='home'),  # Root URL
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
    path('register/', views.register_user, name='register_user'),  # Register URL
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),  # Add this line
    path('edit/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),  # Edit user profile
    path('delete/<int:user_id>/', views.delete_user_profile, name='delete_user_profile'),  # Delete user profile
    path('vcards/', VCardListCreateView.as_view(), name='vcard-list-create'),
    path('vcards/<int:pk>/', VCardDetailView.as_view(), name='vcard-detail'),
    path('userprofiles/', UserProfileListCreateView.as_view(), name='userprofile-list-create'),
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
