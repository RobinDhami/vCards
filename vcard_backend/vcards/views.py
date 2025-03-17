from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, VCard

# View to create a customer
from django.contrib.auth.models import User



def create_customer(request):
    if request.method == 'POST':
        # Get data from the form
        user_name = request.POST['user_name']
        phone = request.POST['phone']
        company_name = request.POST['company_name']
        email = request.POST['email']
        instagram = request.POST.get('instagram', '')  # Using .get to handle optional fields
        facebook = request.POST.get('facebook', '')
        twitter = request.POST.get('twitter', '')
        bio = request.POST.get('bio', '')
        customer_type = request.POST['customer_type']
        
        # Handle profile photo upload
        profile_photo = request.FILES.get('profile_photo')  # This gets the uploaded file

        # Check if username already exists
        if User.objects.filter(username=user_name).exists():
            # Username already exists, inform the user
            return render(request, 'create_customer.html', {'error': 'Username already exists. Please choose another one.'})

        try:
            # Create the User instance (associated with the customer)
            user = User.objects.create_user(
                username=user_name,
                password='defaultpassword',  # You might want to set a default password here or leave it blank
                email=email
            )

            # Create the Customer instance
            customer = Customer.objects.create(
                user=user,  # Associate user
                user_name=user_name,
                phone=phone,
                company_name=company_name,
                email=email,
                instagram=instagram,
                facebook=facebook,
                twitter=twitter,
                bio=bio,
                customer_type=customer_type,
                profile_photo=profile_photo  # Save the uploaded file in the model
            )
            
            # Redirect to the customer's profile page (or another success page)
            return redirect('profile', pk=customer.pk)

        except IntegrityError as e:
            # Handle specific integrity errors
            return render(request, 'create_customer.html', {'error': 'An error occurred while creating the profile.'})

    return render(request, 'create_customer.html')  # Render the form page if GET request


# View to display customer profile
def profile(request):
    try:
        # Try to get the customer profile associated with the logged-in user
        customer_profile = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        # If no customer profile exists, redirect to the create profile page
        return redirect('create_customer')  # Adjust the URL name accordingly

    context = {
        'user': request.user,  # Pass the user object to the template
        'profile': customer_profile,  # Pass the customer's profile
    }

    return render(request, 'customer_profile.html', context)