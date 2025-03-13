# vcards/forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'email', 'website', 'address', 'user_type', 'portfolio_link', 'linkedin', 'twitter']
