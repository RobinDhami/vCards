from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import StudentProfile, ClientProfile, College, Skill
import pandas as pd
from collections import defaultdict
from .models import College
def home(request):
    return render(request, 'home.html')

def profile(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, 'profile5.html', {'student': student})

def admin_dashboard(request):
    colleges = College.objects.prefetch_related('students').all()
    clients = ClientProfile.objects.all()
    return render(request, 'dashboard.html', {
        'colleges': colleges,
        'clients': clients,
    })

def create_student(request):
    if request.method == 'POST':
        college_id = request.POST.get('college')
        college = get_object_or_404(College, id=college_id)

        student = StudentProfile(
            name=request.POST['name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            username=request.POST['username'],
            college=college,
            bio=request.POST.get('bio'),
            password=request.POST['password'],
        )

        if request.FILES.get('profile_photo'):
            student.profile_photo = request.FILES['profile_photo']
        if request.FILES.get('cover_photo'):
            student.cover_photo = request.FILES['cover_photo']

        student.set_password(request.POST['password'])
        student.save()

        skill_ids = request.POST.getlist('skills')
        student.skills.set(skill_ids)

        # Socials
        for field in ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok', 'github', 'figma', 'upwork', 'website']:
            setattr(student, field, request.POST.get(field))

        student.save()
        messages.success(request, 'Student created successfully!')
        return redirect('admin_dashboard')

    skills = Skill.objects.all()
    colleges = College.objects.all()
    return render(request, 'create_student.html', {'skills': skills, 'colleges': colleges})

def edit_student_auth(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        if student.username == request.POST['username'] and student.check_password(request.POST['password']):
            return redirect('edit_student', student_id=student_id)
        messages.error(request, 'Invalid credentials.')
        return redirect('edit_student_auth', student_id=student_id)
    return render(request, 'edit_student_auth.html', {'student_id': student_id})

def edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.phone = request.POST['phone']
        student.email = request.POST['email']
        student.bio = request.POST.get('bio')
        student.skills.set(request.POST.getlist('skills'))

        for field in ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok', 'github', 'figma', 'upwork', 'website']:
            setattr(student, field, request.POST.get(field))

        student.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_dashboard')

    skills = Skill.objects.all()
    return render(request, 'edit_student.html', {'student': student, 'skills': skills})

def bulk_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)

        required_columns = ['name', 'phone', 'email', 'college']
        for col in required_columns:
            if col not in df.columns:
                messages.error(request, f'Missing column: {col}')
                return redirect('bulk_upload')

        for _, row in df.iterrows():
            if pd.isnull(row['name']) or pd.isnull(row['phone']) or pd.isnull(row['college']):
                continue

            college_name = row['college']
            college, _ = College.objects.get_or_create(name=college_name)

            student, created = StudentProfile.objects.get_or_create(
                name=row['name'],
                phone=row['phone'],
                email=row.get('email', ''),
                college=college
            )
            student.save()

        messages.success(request, 'Bulk upload successful.')
        return redirect('admin_dashboard')

    return render(request, 'bulk_upload.html')
    
def college_details(request, college_id):
    college = get_object_or_404(College, id=college_id)
    students = college.students.all()
    return render(request, 'college_details.html', {'college': college, 'students': students})


def add_college(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slogan = request.POST.get('slogan')
        address = request.POST.get('address')
        logo = request.FILES.get('logo')
        website = request.POST.get('website')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')

        college = College(
            name=name,
            slogan=slogan,
            address=address,
            logo=logo,
            website=website,
            email=email,
            phone=phone,
            description=description
        )
        college.save()
        messages.success(request, "College added successfully!")
        return redirect('admin_dashboard')  # or wherever you want to redirect

    return render(request, 'add_college.html')


def edit_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    if request.method == 'POST':
        college.name = request.POST.get('name')
        college.slogan = request.POST.get('slogan')
        college.address = request.POST.get('address')
        if request.FILES.get('logo'):
            college.logo = request.FILES['logo']
        college.website = request.POST.get('website')
        college.email = request.POST.get('email')
        college.phone = request.POST.get('phone')
        college.description = request.POST.get('description')
        college.save()
        messages.success(request, "College updated successfully!")
        return redirect('college_details', college_id=college.id)
    return render(request, 'edit_college.html', {'college': college})

def delete_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    if request.method == 'POST':
        college.delete()
        messages.success(request, "College deleted successfully!")
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete_college.html', {'college': college})