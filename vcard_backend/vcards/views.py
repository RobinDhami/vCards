from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Student, Skill
from django.contrib import messages
import pandas as pd
from collections import defaultdict




def home(request):
    return render(request,'home.html')
def profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'profile5.html', {'student': student})


def admin_dashboard(request):
    students = Student.objects.all().order_by('college', 'name')
    students_by_college = defaultdict(list)

    for student in students:
        students_by_college[student.college].append(student)

    return render(request, 'dashboard.html', {
        'students_by_college': dict(students_by_college)
    })

def create_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST.get('address')
        college = request.POST.get('college')
        education_completed = request.POST.get('education_completed')
        bio = request.POST.get('bio')
        about_me = request.POST.get('about_me')

        # Create student instance
        student = Student(
            name=name,
            phone=phone,
            email=email,
            username=username,
            address=address,
            college=college,
            education_completed=education_completed,
            bio=bio,
            about_me=about_me
        )
        student.set_password(password)

        # Handle file uploads
        if request.FILES.get('photo'):
            student.photo = request.FILES['photo']
        if request.FILES.get('cover_photo'):
            student.cover_photo = request.FILES['cover_photo']
        if request.FILES.get('resume'):
            student.resume = request.FILES['resume']

        student.save()

        # Skills
        skill_ids = request.POST.getlist('skills')
        student.skills.set(skill_ids)

        # Social links
        student.facebook = request.POST.get('facebook')
        student.instagram = request.POST.get('instagram')
        student.twitter = request.POST.get('twitter')
        student.youtube = request.POST.get('youtube')
        student.figma = request.POST.get('figma')
        student.github = request.POST.get('github')
        student.upwork = request.POST.get('upwork')
        student.other = request.POST.get('other')

        student.save()

        messages.success(request, 'Student created successfully!')
        return redirect('admin_dashboard')

    skills = Skill.objects.all()
    return render(request, 'create_student.html', {'skills': skills})


def edit_student_auth(request, student_id):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        student = get_object_or_404(Student, id=student_id)
        if student.username == username and student.check_password(password):
            return redirect('edit_student', student_id=student_id)
        messages.error(request, 'Invalid credentials.')
        return redirect('edit_student_auth', student_id=student_id)
    return render(request, 'edit_student_auth.html', {'student_id': student_id})

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.phone = request.POST['phone']
        student.email = request.POST['email']
        student.skills.set(request.POST.getlist('skills'))
        student.facebook = request.POST.get('facebook')
        student.instagram = request.POST.get('instagram')
        student.twitter = request.POST.get('twitter')
        student.youtube = request.POST.get('youtube')
        student.figma = request.POST.get('figma')
        student.github = request.POST.get('github')
        student.upwork = request.POST.get('upwork')
        student.other = request.POST.get('other')
        student.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_dashboard')
    skills = Skill.objects.all()
    return render(request, 'edit_student.html', {'student': student, 'skills': skills})
# views.py


def bulk_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']

        # Read Excel with pandas
        df = pd.read_excel(excel_file)

        required_columns = ['name', 'address', 'phone']
        for col in required_columns:
            if col not in df.columns:
                messages.error(request, f'Missing column: {col}')
                return redirect('bulk_upload')

        # Optional columns: college, email, etc.
        for _, row in df.iterrows():
            name = row['name']
            address = row['address']
            phone = row['phone']

            if pd.isnull(name) or pd.isnull(address) or pd.isnull(phone):
                continue  # skip incomplete rows

            # Find by name — update or create
            student, created = Student.objects.get_or_create(name=name)

            student.address = address
            student.phone = phone

            if 'college' in df.columns:
                student.college = row['college'] if pd.notnull(row['college']) else student.college

            if 'email' in df.columns:
                student.email = row['email'] if pd.notnull(row['email']) else student.email

            student.save()

        messages.success(request, 'Bulk upload successful.')
        return redirect('admin_dashboard')

    return render(request, 'bulk_upload.html')

