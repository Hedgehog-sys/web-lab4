from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher, Group

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Group)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'group_rel')
    list_filter = ('group_rel',)

    def get_username(self, obj):
        return obj.user.username if obj.user else "Пользователь не привязан"
    get_username.short_description = 'Логин'

admin.site.register(Teacher)
