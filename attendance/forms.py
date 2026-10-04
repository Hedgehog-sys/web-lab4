from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import Student, Group

def validate_filesize(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Размер файла не должен превышать {max_mb} МБ")

class StudentAvatarForm(forms.ModelForm):
    """Форма загрузки аватара (Задание 2)"""
    avatar = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_filesize
        ],
        label="Аватар"
    )

    class Meta:
        model = Student
        fields = ["avatar"]


class StudentFilterForm(forms.Form):
    """Форма GET-фильтрации списка студентов (Задание 3)"""
    last_name = forms.CharField(label="Часть фамилии", required=False)
    group = forms.ModelChoiceField(label="Конкретная группа", queryset=Group.objects.all(), required=False)
    group_name_part = forms.CharField(label="Часть названия группы", required=False)
