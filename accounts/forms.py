from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")


