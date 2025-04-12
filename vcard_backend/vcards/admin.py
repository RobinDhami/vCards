from django.contrib import admin
from .models import Customer, VIPProfile, VCard

# Register the models without custom ModelAdmin classes
admin.site.register(Customer)
admin.site.register(VIPProfile)
admin.site.register(VCard)
