from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, VCard, VIPProfile, CustomerType
from django.http import JsonResponse
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
        user = request.user

        # Extract form data
        customer_type = request.POST.get('customer_type', CustomerType.GENERAL)

        customer = Customer.objects.create(
            user=user,
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
        
        # Create a VIP profile if the user is VIP
        if customer_type == CustomerType.VIP:
            VIPProfile.objects.create(customer=customer)

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
        vcard.portfolio_link = request.POST['portfolio_link']
        vcard.save()
        return redirect('dashboard')
    
    return render(request, 'create_vcard.html', {'vcard': vcard})


# ============================
# EDIT CUSTOMER VIEW
# ============================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

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
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'customer': customer})


# ============================
# CUSTOMER PROFILE VIEW
# ============================
# ============================
# CUSTOMER PROFILE VIEW
# ============================
@login_required
def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Increment the vcard_views when the profile is viewed
    if customer.is_vip:
        vip_profile = customer.vip_profile
        vip_profile.vcard_views += 1
        vip_profile.save()

    # Decide which template to use based on customer type
    template_name = 'vprofile.html' if customer.is_vip else 'gprofile.html'

    return render(request, template_name, {'customer': customer})



# ============================
# DOWNLOAD VCARD
# ============================
from django.http import HttpResponse

def download_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{customer.user_name}
ORG:{customer.company_name}
EMAIL:{customer.email}
TEL:{customer.phone}
URL:{customer.instagram if customer.instagram else ''} 
URL:{customer.linkedin if customer.linkedin else ''}
URL:{customer.twitter if customer.twitter else ''}
URL:{customer.tiktok if customer.tiktok else ''}
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

    if customer.is_vip:
        vip_profile = get_object_or_404(VIPProfile, customer=customer)
        
        if request.method == 'POST':
            entered_password = request.POST.get('password')
            
            if entered_password == vip_profile.password:
                return redirect('analytics', customer_id=customer.id)  # Redirect to analytics page if password is correct
            else:
                messages.error(request, 'Incorrect password! Please try again.')

        return render(request, 'password_check.html', {'customer': customer})

    return redirect('dashboard')  # If not VIP, redirect to dashboard

# ============================
# ANALYTICS VIEW
# ============================
@login_required
def analytics(request, customer_id):
    # Get the customer object
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if the customer is VIP
    if customer.is_vip:
        # Access the related VIPProfile
        vip_profile = customer.vip_profile  # Get the VIPProfile to access analytics fields
        vcard_views = vip_profile.vcard_views
        vcard_taps = vip_profile.vcard_taps
        vcard_saves = vip_profile.vcard_saves

        # Debugging: Print the current values to ensure they are correct
        print(f"vcard_saves: {vcard_saves}, vcard_taps: {vcard_taps}, vcard_views: {vcard_views}")

        # Render the template with the analytics data
        return render(request, 'analytics.html', {
            'customer': customer,
            'vcard_views': vcard_views,
            'vcard_taps': vcard_taps,
            'vcard_saves': vcard_saves
        })

    # Redirect to dashboard if the customer is not VIP
    return redirect('dashboard')
# ============================
# TAPPING VCARD (Increment vcard_taps)
# ============================
@login_required
def tap_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        # Increment vcard_taps when VIP user's vcard is tapped
        vip_profile = customer.vip_profile
        vip_profile.vcard_taps += 1
        vip_profile.save()

        # Display the updated tap count
        return render(request, 'vip_analytics.html', {
            'customer': customer,
            'vcard_taps': vip_profile.vcard_taps,  # Use vip_profile.vcard_taps here
        })

    return redirect('dashboard')  # Redirect to dashboard if not a VIP


# ============================
# SAVING VCARD (Increment vcard_saves)
# ============================
@login_required
def save_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        vip_profile = customer.vip_profile  # Access the related VIPProfile
        vip_profile.vcard_saves += 1  # Increment the save count
        vip_profile.save()  # Save the updated profile

        # Optional: Add logging to confirm the increment is happening
        print(f"vCard saved for {customer.username}. New vcard_saves count: {vip_profile.vcard_saves}")

    else:
        # Redirect or show an error message if not a VIP
        return redirect('error_page')  # Or an appropriate page for non-VIP users

    return redirect('vcard_detail', customer_id=customer_id)  # Redirect to the vCard detail or another page

@login_required
def admin_analytics(request):
    if not request.user.is_staff:
        return redirect('dashboard')  # Redirect non-admin users to the dashboard

    # Get the total taps for all customers
    total_taps = Customer.objects.aggregate(total_taps=models.Sum('vcard_taps'))['total_taps'] or 0
    
    return render(request, 'admin_analytics.html', {
        'total_taps': total_taps,
    })

@login_required
def edit_vip_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Ensure VIP profile exists or create one
    vip_profile, created = VIPProfile.objects.get_or_create(customer=customer)

    if request.method == 'POST':
        vip_profile.primary_color = request.POST.get('primary_color', vip_profile.primary_color)
        vip_profile.secondary_color = request.POST.get('secondary_color', vip_profile.secondary_color)
        vip_profile.accent_color = request.POST.get('accent_color', vip_profile.accent_color)

        # Handle company logo upload
        if 'company_logo' in request.FILES:
            vip_profile.company_logo = request.FILES['company_logo']

        # Handle custom background color
        vip_profile.custom_background = request.POST.get('custom_background', vip_profile.custom_background)

        vip_profile.save()
        
        # Redirect to the same page after saving the changes
        return redirect('edit_vip_profile', customer_id=customer.id)

    return render(request, 'edit_vip_profile.html', {'customer': customer, 'vip_profile': vip_profile})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, VIPProfile, CustomerType
from django.contrib import messages

@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if the user is authorized to edit this customer (only the user themselves or staff can edit)
    if request.user != customer.user and not request.user.is_staff:
        return redirect('dashboard')  # Redirect if the user is not allowed to edit this customer
    
    # Check if the customer is a VIP and fetch their VIP profile
    vip_profile = None
    if customer.is_vip:
        vip_profile = customer.vip_profile

    if request.method == 'POST':
        # Handle form data and update customer info
        customer.user_name = request.POST.get('user_name', customer.user_name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.company_name = request.POST.get('company_name', customer.company_name)
        customer.email = request.POST.get('email', customer.email)

        # Handle customer type change (general to VIP or vice versa)
        customer_type = request.POST.get('customer_type', customer.customer_type)
        if customer_type != customer.customer_type:
            customer.customer_type = customer_type
            if customer.customer_type == CustomerType.VIP and not customer.is_vip:
                # Create a VIP profile when switching to VIP
                vip_profile = VIPProfile.objects.create(customer=customer)
            elif customer.customer_type != CustomerType.VIP and customer.is_vip:
                # Remove VIP profile when switching away from VIP
                if vip_profile:
                    vip_profile.delete()

        # Handle file uploads for profile and cover photos
        if 'profile_photo' in request.FILES:
            customer.profile_photo = request.FILES['profile_photo']
        
        if 'cover_photo' in request.FILES:
            customer.cover_photo = request.FILES['cover_photo']

        # Handle VIP-specific fields
        if vip_profile:
            vip_profile.primary_color = request.POST.get('primary_color', vip_profile.primary_color)
            vip_profile.secondary_color = request.POST.get('secondary_color', vip_profile.secondary_color)
            vip_profile.accent_color = request.POST.get('accent_color', vip_profile.accent_color)

            if 'company_logo' in request.FILES:
                vip_profile.company_logo = request.FILES['company_logo']

            vip_profile.custom_background = request.POST.get('custom_background', vip_profile.custom_background)

            vip_profile.save()

        customer.save()
        messages.success(request, "Your information has been updated successfully!")
        return redirect('dashboard')  # Redirect to dashboard after saving changes

    # Prepopulate form with existing customer data
    return render(request, 'edit_customer.html', {
        'customer': customer,
        'vip_profile': vip_profile,
    })
