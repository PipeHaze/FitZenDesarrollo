from django import forms
from django.contrib.auth.forms import(AuthenticationForm, PasswordResetForm, SetPasswordForm)
from django.forms.widgets import FileInput
from .models import UserBase
from django.contrib.auth.forms import UserChangeForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Ingresa Tu Correo', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'login-pwd',
        }
    ))