from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .models import Customer, VCard, VIPProfile, CustomerType
from vcards import models

# ============================
# DASHBOARD VIEW
# ============================
@login_required
def dashboard(request):
    customers = Customer.objects.prefetch_related('vcard', 'vip_profile').all()
    return render(request, 'dashboard.html', {'customers': customers})


# ============================
# CREATE CUSTOMER VIEW
# ============================
@login_required
def create_customer(request):
    if request.method == 'POST':
        # Ensure necessary fields are provided
        required_fields = ['user_name', 'phone', 'company_name', 'email']
        if not all(request.POST.get(field) for field in required_fields):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'create_customer.html')

        # Extract form data
        customer_type = request.POST.get('customer_type', CustomerType.GENERAL)
        customer = Customer.objects.create(
            user=request.user,
            user_name=request.POST['user_name'],
            phone=request.POST['phone'],
            company_name=request.POST['company_name'],
            email=request.POST['email'],
            profile_photo=request.FILES.get('profile_photo'),
            cover_photo=request.FILES.get('cover_photo'),
            instagram=request.POST.get('instagram'),
            facebook=request.POST.get('facebook'),
            twitter=request.POST.get('twitter'),
            linkedin=request.POST.get('linkedin'),
            youtube=request.POST.get('youtube'),
            tiktok=request.POST.get('tiktok'),
            whatsapp=request.POST.get('whatsapp'),
            personal_website=request.POST.get('personal_website'),
            bio=request.POST.get('bio'),
            customer_type=customer_type
        )

        # Create VIP profile if customer is VIP
        if customer_type == CustomerType.VIP:
            VIPProfile.objects.create(customer=customer)

        messages.success(request, "Customer created successfully!")
        return redirect('dashboard')

    return render(request, 'create_customer.html')


# ============================
# CREATE OR UPDATE VCARD
# ============================
@login_required
def create_vcard(request):
    customer = get_object_or_404(Customer, user=request.user)
    vcard, created = VCard.objects.get_or_create(customer=customer)
    
    if request.method == 'POST':
        vcard.portfolio_link = request.POST.get('portfolio_link', vcard.portfolio_link)
        vcard.save()
        messages.success(request, "vCard updated successfully!")
        return redirect('dashboard')
    
    return render(request, 'create_vcard.html', {'vcard': vcard})


# ============================
# VCARD DETAIL VIEW
# ============================
@login_required
def vcard_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    vcard = VCard.objects.filter(customer=customer).first()
    return render(request, 'vcard_detail.html', {'customer': customer, 'vcard': vcard})


# ============================
# DELETE CUSTOMER VIEW
# ============================
@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted successfully!")
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'customer': customer})


# ============================
# CUSTOMER PROFILE VIEW
# ============================
def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Increment views for VIP profiles
    if customer.is_vip:
        vip_profile = customer.vip_profile
        vip_profile.vcard_views += 1
        vip_profile.save()

    # Use separate templates for VIP and General customers
    template_name = 'vprofile.html' if customer.is_vip else 'gprofile.html'
    return render(request, template_name, {'customer': customer})


# ============================
# DOWNLOAD VCARD
# ============================
def download_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{customer.user_name}
ORG:{customer.company_name}
EMAIL:{customer.email}
TEL:{customer.phone}
URL:{customer.instagram or ''} 
URL:{customer.linkedin or ''} 
URL:{customer.twitter or ''} 
URL:{customer.tiktok or ''} 
END:VCARD
"""
    response = HttpResponse(vcard_content, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{customer.user_name}.vcf"'
    return response


# ============================
# PASSWORD CHECK VIEW (For VIP)
# ============================
@login_required
def password_check(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        entered_password = request.POST.get('entered_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the entered password and new passwords
        if not check_password(entered_password, customer.user.password):
            messages.error(request, "Incorrect current password.")
            return redirect('edit_customer', customer_id=customer.id)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('edit_customer', customer_id=customer.id)

        if new_password:
            customer.user.set_password(new_password)
            customer.user.save()
            update_session_auth_hash(request, customer.user)  # Keep user logged in
            messages.success(request, "Password updated successfully!")
            return redirect('edit_customer', customer_id=customer.id)

    return redirect('dashboard')  # Redirect if the method is not POST


# ============================
# ANALYTICS VIEW (For VIPs)
# ============================
@login_required
def analytics(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if customer.is_vip:
        vip_profile = customer.vip_profile
        vcard_views = vip_profile.vcard_views
        vcard_taps = vip_profile.vcard_taps
        vcard_saves = vip_profile.vcard_saves
        return render(request, 'analytics.html', {
            'customer': customer,
            'vcard_views': vcard_views,
            'vcard_taps': vcard_taps,
            'vcard_saves': vcard_saves
        })
    return redirect('dashboard')


# ============================
# TAPPING VCARD (Increment vcard_taps)
# ============================
def tap_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        vip_profile = customer.vip_profile
        vip_profile.vcard_taps += 1
        vip_profile.save()
        return render(request, 'vip_analytics.html', {
            'customer': customer,
            'vcard_taps': vip_profile.vcard_taps
        })

    return redirect('dashboard')


# ============================
# SAVING VCARD (Increment vcard_saves)
# ============================
def save_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        vip_profile = customer.vip_profile
        vip_profile.vcard_saves += 1
        vip_profile.save()

        # Optional logging for debugging
        print(f"vCard saved for {customer.user_name}. New vcard_saves count: {vip_profile.vcard_saves}")

    return redirect('vcard_detail', customer_id=customer.id)


# ============================
# ADMIN ANALYTICS VIEW
# ============================
@login_required
def admin_analytics(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    # Aggregate total vcard taps across all customers
    total_taps = Customer.objects.aggregate(total_taps=models.Sum('vcard_taps'))['total_taps'] or 0
    return render(request, 'admin_analytics.html', {'total_taps': total_taps})


# ============================
# EDIT VIP PROFILE
# ============================
@login_required
def edit_vip_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    vip_profile = get_object_or_404(VIPProfile, customer=customer)

    if request.method == 'POST':
        customer.user_name = request.POST.get('user_name', customer.user_name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.email = request.POST.get('email', customer.email)
        customer.company_name = request.POST.get('company_name', customer.company_name)

        # Update VIPProfile fields
        vip_profile.primary_color = request.POST.get('primary_color', vip_profile.primary_color)
        vip_profile.secondary_color = request.POST.get('secondary_color', vip_profile.secondary_color)
        vip_profile.accent_color = request.POST.get('accent_color', vip_profile.accent_color)
        vip_profile.custom_background = request.POST.get('custom_background', vip_profile.custom_background)

        # Save customer and VIP profile
        customer.save()
        vip_profile.save()

        messages.success(request, "VIP profile updated successfully!")
        # return redirect('customer_profile', customer_id=customer.id)

    return render(request, 'edit_vip_profile.html', {'customer': customer, 'vip_profile': vip_profile})


# ============================
# EDIT CUSTOMER PROFILE
# ============================
@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.user != customer.user and not request.user.is_staff:
        return redirect('dashboard')  # Prevent unauthorized edits

    vip_profile = None
    if customer.is_vip:
        vip_profile = customer.vip_profile

    if request.method == 'POST':
        # Handle form updates
        customer.user_name = request.POST.get('user_name', customer.user_name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.company_name = request.POST.get('company_name', customer.company_name)
        customer.email = request.POST.get('email', customer.email)

        customer.save()

        # Handle VIP-specific updates
        if vip_profile:
            vip_profile.primary_color = request.POST.get('primary_color', vip_profile.primary_color)
            vip_profile.secondary_color = request.POST.get('secondary_color', vip_profile.secondary_color)
            vip_profile.accent_color = request.POST.get('accent_color', vip_profile.accent_color)
            vip_profile.save()

        messages.success(request, "Customer information updated successfully!")
        return redirect('dashboard')

    return render(request, 'edit_customer.html', {'customer': customer, 'vip_profile': vip_profile})
