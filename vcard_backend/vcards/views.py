from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, VCard, VIPProfile, CustomerType

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
# CREATE OR UPDATE VCard
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

@login_required
def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Decide which template to use based on customer type
    template_name = 'vprofile.html' if customer.is_vip else 'gprofile.html'

    return render(request, template_name, {'customer': customer})

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
