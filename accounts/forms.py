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
    captcha_num1 = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    captcha_num2 = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    captcha_answer = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        num1 = cleaned_data.get('captcha_num1') or 0
        num2 = cleaned_data.get('captcha_num2') or 0
        answer = cleaned_data.get('captcha_answer') or -1
        if num1 + num2 != answer:
            raise forms.ValidationError('Captcha wrong! / கேப்ட்சா தவறானது!')
        return cleaned_data