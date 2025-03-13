# serializers.py
from rest_framework import serializers
from .models import VCard, UserProfile

class VCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VCard
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'website', 'address', 'qr_code']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'website', 'address', 'user_type', 'portfolio_link', 'linkedin', 'twitter', 'qr_code']
