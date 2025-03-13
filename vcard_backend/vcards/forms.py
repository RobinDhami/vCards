# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'email', 'user_type', 'profile_picture', 'cover_photo', 'bio', 'facebook', 'instagram', 'linkedin', 'portfolio_link', 'twitter']
