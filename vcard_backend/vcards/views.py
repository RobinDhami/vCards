from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .models import Customer, VCard, VIPProfile, CustomerType
from vcards import models
from django.contrib.auth.models import User
from .models import Student


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
from django.contrib.auth.hashers import make_password

@login_required
def create_customer(request):
    if request.method == 'POST':
        # Extract form data
        customer_type = request.POST.get('customer_type', CustomerType.GENERAL)
        user_email = request.POST['email']
        user_username = request.POST['user_name']  # Get the username from form input

        # Check if the user already exists
        existing_user = User.objects.filter(username=user_username).first()

        if existing_user:
            # Check if the user already has a linked customer profile
            if hasattr(existing_user, 'customer'):
                messages.error(request, "This user already has a customer profile.")
                return render(request, 'create_customer.html')
            else:
                # The user exists but doesn't have a customer profile, so you can create one.
                customer = Customer.objects.create(
                    user=existing_user,
                    user_name=user_username,
                    phone=request.POST['phone'],
                    company_name=request.POST['company_name'],
                    email=user_email,
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
                if customer_type == CustomerType.VIP:
                    VIPProfile.objects.create(customer=customer)
                messages.success(request, "Customer created successfully!")
                return redirect('dashboard')

        else:
            # Check if the passwords match
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'create_customer.html')

            # Create a new User object with hashed password
            user = User.objects.create_user(
                username=user_username,
                email=user_email,
                password=password  # Ensure password is hashed by create_user()
            )

            # Now create the associated customer profile
            customer = Customer.objects.create(
                user=user,
                user_name=user_username,
                phone=request.POST['phone'],
                company_name=request.POST['company_name'],
                email=user_email,
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
def password_check(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        entered_password = request.POST.get('entered_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the entered password is correct
        if not check_password(entered_password, customer.user.password):
            messages.error(request, "Incorrect current password.")
            return render(request, 'edit_vip_profile.html', {'customer': customer})  # Re-render the edit page with error

        # Validate new passwords
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'edit_vip_profile.html', {'customer': customer})  # Re-render the edit page with error

        if new_password:
            # Update the password if the new one is valid
            customer.user.set_password(new_password)
            customer.user.save()
            update_session_auth_hash(request, customer.user)  # Keep user logged in
            messages.success(request, "Password updated successfully!")
            return redirect('edit_vip_profile', customer_id=customer.id)  # Redirect to edit page

    # Default redirection if not POST
    return redirect('customer_profile', customer_id=customer.id) 
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


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, VIPProfile

def edit_vip_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    vip_profile = get_object_or_404(VIPProfile, customer=customer)

    if request.method == 'POST':
        entered_username = request.POST.get('username')
        entered_password = request.POST.get('password')

        # Check if the entered username matches the customer
        if entered_username == customer.user_name:
            # Now, authenticate using the associated User model's password
            user = customer.user  # Assuming 'user' is a ForeignKey to Django's User model
            
            # Check if the entered password is correct for this user
            if user.check_password(entered_password):
                # If authentication is successful, proceed with profile editing
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
                return redirect('edit_vip_profile', customer_id=customer.id)  # Redirect to VIP edit page after success
            else:
                messages.error(request, "Incorrect username or password. Please try again.")
        else:
            messages.error(request, "Incorrect username or password. Please try again.")

        # If we reach here, the password was incorrect, so re-render the form with error
        return render(request, 'vprofile.html', {'customer': customer, 'vip_profile': vip_profile})

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



def student_profile(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'student_profile.html', {'student': student})
