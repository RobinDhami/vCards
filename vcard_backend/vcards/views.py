from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Student, Skill
from django.contrib import messages

def admin_dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html', {'students': students})

def create_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        skill_ids = request.POST.getlist('skills')
        student = Student(name=name, phone=phone, email=email, username=username)
        student.set_password(password)
        student.save()
        student.skills.set(skill_ids)
        # Set social links
        student.facebook = request.POST.get('facebook')
        student.instagram = request.POST.get('instagram')
        student.twitter = request.POST.get('twitter')
        student.youtube = request.POST.get('youtube')
        student.figma = request.POST.get('figma')
        student.github = request.POST.get('github')
        student.upwork = request.POST.get('upwork')
        student.other = request.POST.get('other')
        student.save()
        messages.success(request, 'Student created successfully.')
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
