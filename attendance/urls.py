from django.urls import path
from . import views

urlpatterns = [
    path('redirect/', views.profile_redirect_view, name='profile_redirect'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('common/', views.common_dashboard, name='common_dashboard'),
    
    # Новые маршруты Практики 4
    path('upload-raw/', views.upload_raw, name='upload_raw'),
    path('avatar-update/', views.student_avatar_update, name='student_avatar_update'),
    path('students-list/', views.student_list_view, name='student_list_view'),
]
