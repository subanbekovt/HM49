from django import forms
from django.forms import widgets
from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "type"]
        error_messages = {
            'title': {
                'required': "Поле обязательно для заполнения",
                'max_length': "Не более 200 знаков"
            },
            'description': {
                'max_length': "Не более 2000 знаков"
            },
            'status': {
                'required': "Поле обязательно для заполнения",
                'max_length': "Не более 200 знаков"
            },
            'type': {
                'required': "Поле обязательно для заполнения",
                'max_length': "Не более 200 знаков"
            }
        }
        help_texts = {
            'name': "Введите свое название",
            'description': "Введите описание задачи",
            'status': "Выберите статус задачи",
            'type': "Выберите тип задачи"
        }
