from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    district = forms.CharField(max_length=100, required=True)
    taluk = forms.CharField(max_length=100, required=False)
    village = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'district', 'taluk', 'village', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())