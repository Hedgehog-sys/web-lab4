import os
import uuid
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from .models import Student, Group
from .forms import StudentAvatarForm, StudentFilterForm

@login_required
def profile_redirect_view(request):
    user = request.user
    if user.is_student:
        return redirect('/attendance/student/')
    elif user.is_teacher:
        return redirect('/attendance/teacher/')
    else:
        return redirect('/attendance/common/')

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return HttpResponseForbidden("Доступ запрещен.")
    return render(request, 'attendance/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("Доступ запрещен.")
    return render(request, 'attendance/teacher_dashboard.html')

@login_required
def common_dashboard(request):
    return render(request, 'attendance/common_dashboard.html')



def upload_raw(request):
    """Ручная загрузка файла частями (Задание 1)"""
    if request.method == "POST" and request.FILES.get("file_upload"):
        f = request.FILES["file_upload"]
        ext = os.path.splitext(f.name)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        
        dest = Path(settings.MEDIA_ROOT) / "raw" / unique_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        with dest.open("wb+") as out:
            for chunk in f.chunks():
                out.write(chunk)
        return HttpResponse(f"Файл успешно загружен частями в: {dest}")
    return render(request, 'attendance/upload_raw.html')


@login_required
def student_avatar_update(request):
    """Загрузка аватара с проверкой прав доступа (Задание 2)"""
    if not request.user.is_student:
        return HttpResponseForbidden("Изменять аватар могут только студенты.")
    
    student = request.user.student
    if request.method == "POST":
        form = StudentAvatarForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/attendance/student/')
    else:
        form = StudentAvatarForm(instance=student)
    return render(request, 'attendance/avatar_form.html', {'form': form})


def student_list_view(request):
    """Список студентов с GET-фильтрацией (Задание 3)"""
    students = Student.objects.all()
    form = StudentFilterForm(request.GET)
    
    if form.is_valid():
        lname = form.cleaned_data.get('last_name')
        grp = form.cleaned_data.get('group')
        grp_part = form.cleaned_data.get('group_name_part')

        if lname:
            students = students.filter(user__last_name__icontains=lname)
        if grp:
            students = students.filter(group_rel=grp)
        if grp_part:
            students = students.filter(group_rel__name__icontains=grp_part)
    else:
        students = Student.objects.none()
        
    return render(request, 'attendance/students_list.html', {'form': form, 'students': students})
