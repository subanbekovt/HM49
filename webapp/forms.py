from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "types"]
        widgets = {
            'types': widgets.CheckboxSelectMultiple
        }
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
            'types': {
                'required': "Поле обязательно для заполнения",
                'max_length': "Не более 200 знаков"
            }
        }
        help_texts = {
            'name': "Введите свое название",
            'description': "Введите описание задачи",
            'status': "Выберите статус задачи",
            'types': "Выберите тип задачи"
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        description = cleaned_data['description']
        if len(title) < 5:
            self.add_error('title', ValidationError(f'Значение должно быть длиннее 5 символов {title} не подходит'))
        if title == description:
            raise ValidationError('Название и описание задачи не должны совпадать. Опишите задачу как можно подробнее!')
        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = []
        widgets = {
            'created_at': widgets.DateInput(attrs={'type': 'date'})
        }
