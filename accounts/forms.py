from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "first_name", "last_name", "password1", "password2", "email")

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


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('git', 'about', 'avatar')


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label='Старый пароль', strip=False, widget=forms.PasswordInput)
    password = forms.CharField(label='Новый пароль', strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password_confirm']


