from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, VCard, VIPProfile, CustomerType
from django.http import JsonResponse


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
@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if the current user is an admin or VIP
    if customer.is_vip and not request.user.is_staff:  # Only prompt non-admin VIP users for password
        return redirect('password_check', customer_id=customer.id)  # Redirect to password check page for non-admin VIPs

    if request.method == 'POST':
        customer.user_name = request.POST['user_name']
        customer.phone = request.POST['phone']
        customer.company_name = request.POST['company_name']
        customer.email = request.POST['email']
        customer.customer_type = request.POST.get('customer_type', CustomerType.GENERAL)

        # Handle profile photo update
        if 'profile_photo' in request.FILES:
            customer.profile_photo = request.FILES['profile_photo']

        # Handle cover photo update
        if 'cover_photo' in request.FILES:
            customer.cover_photo = request.FILES['cover_photo']

        customer.save()
        return redirect('dashboard')

    return render(request, 'edit_customer.html', {'customer': customer})


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
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        vip_profile = customer.vip_profile  # Access the related VIPProfile model
        
        # Access analytics data from VIPProfile
        vcard_views = vip_profile.vcard_views
        vcard_taps = vip_profile.vcard_taps
        vcard_saves = vip_profile.vcard_saves
        
        return render(request, 'analytics.html', {
            'customer': customer,
            'vcard_views': vcard_views,
            'vcard_taps': vcard_taps,
            'vcard_saves': vcard_saves
        })

    return redirect('dashboard')  # If not VIP, redirect to the dashboard

# ============================
# TAPPING VCARD (Increment vcard_taps)
# ============================
@login_required
def tap_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        # Increment vcard_taps when VIP user's vcard is tapped
        customer.vcard_taps += 1
        customer.save()

        # You can then display the updated tap count
        return render(request, 'vip_analytics.html', {
            'customer': customer,
            'vcard_taps': customer.vcard_taps,
        })

    return redirect('dashboard')  # Redirect to dashboard if not a VIP

# ============================
# SAVING VCARD (Increment vcard_saves)
# ============================
@login_required
def save_vcard(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.is_vip:
        vip_profile = customer.vip_profile
        vip_profile.vcard_saves += 1
        vip_profile.save()

    return redirect('vcard_detail', customer_id=customer_id)  # Or any redirect after saving

@login_required
def admin_analytics(request):
    if not request.user.is_staff:
        return redirect('dashboard')  # Redirect non-admin users to the dashboard

    # Get the total taps for all customers
    total_taps = Customer.objects.aggregate(total_taps=models.Sum('vcard_taps'))['total_taps'] or 0
    
    return render(request, 'admin_analytics.html', {
        'total_taps': total_taps,
    })
