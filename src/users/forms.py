from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm):
#         model = User
#         fields = ('email',)


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = User
#         fields = ('email',)


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=200, required=True, widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', max_length=100, required=True, widget=forms.PasswordInput())