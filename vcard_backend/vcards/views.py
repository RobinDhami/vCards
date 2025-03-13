# Import necessary modules
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserProfileForm

# Home View
def home(request):
    return render(request, 'home.html')

# VCard Views (already existing)
from rest_framework import generics
from .models import VCard
from .serializers import UserProfileSerializer, VCardSerializer

class VCardListCreateView(generics.ListCreateAPIView):
    queryset = VCard.objects.all()
    serializer_class = VCardSerializer

class VCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VCard.objects.all()
    serializer_class = VCardSerializer

# UserProfile Views (existing views for list and registration)
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# Dashboard View (to display all registered users)
def dashboard(request):
    users = UserProfile.objects.all()
    return render(request, 'dashboard.html', {'users': users})

# Register User View (to register a new user)
def register_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after successful registration
    else:
        form = UserProfileForm()
    
    return render(request, 'register_user.html', {'form': form})

# User Profile View
def user_profile(request, user_id):
    # Retrieve the user by ID or show a 404 error if not found
    user = get_object_or_404(UserProfile, pk=user_id)

    # Check the user's type (VIP or Normal) and render the appropriate profile template
    if user.user_type == 'VIP':
        return render(request, 'vip_profile.html', {'user': user})
    else:
        return render(request, 'normal_profile.html', {'user': user})
