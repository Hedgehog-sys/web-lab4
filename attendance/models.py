import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    @property
    def is_student(self):
        return hasattr(self, 'student')

    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')


class Group(models.Model):
    """Модель учебной группы (Задание 3)"""
    name = models.CharField(max_length=50, verbose_name="Название группы")

    def __str__(self):
        return self.name


def avatar_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    uid = uuid.uuid4().hex
    return f"avatars/{uid}{ext}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_rel = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")
    avatar = models.ImageField(upload_to=avatar_upload_to, default='avatars/default.jpg')

    def __str__(self):
       if self.user and (self.user.last_name or self.user.first_name):
           return f"{self.user.last_name} {self.user.first_name}".strip()
       return f"Студент: {self.user.username if self.user else 'ID ' + str(self.id)}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, default="ЭAFU")
