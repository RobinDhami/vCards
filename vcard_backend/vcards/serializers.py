from rest_framework import serializers
from .models import VCard, UserProfile

class VCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VCard
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'website', 'address', 'qr_code']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'user_type', 'profile_picture', 'cover_photo', 'bio', 'facebook', 'instagram', 'linkedin', 'portfolio_link', 'twitter', 'qr_code']
