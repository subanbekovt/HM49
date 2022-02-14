from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

    def clean_first_name(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        if first_name:
            return cleaned_data
        else:
            raise ValidationError('Заполните это поле!')

    def clean_first_name(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        if first_name:
            return cleaned_data
        else:
            raise ValidationError('Пожалуйста заполните это поле!')

