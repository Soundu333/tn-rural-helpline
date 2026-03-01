from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import CustomUser

TN_DISTRICTS = [
    ('', 'Select District / மாவட்டம் தேர்ந்தெடு'),
    ('Ariyalur', 'Ariyalur'),
    ('Chengalpattu', 'Chengalpattu'),
    ('Chennai', 'Chennai'),
    ('Coimbatore', 'Coimbatore'),
    ('Cuddalore', 'Cuddalore'),
    ('Dharmapuri', 'Dharmapuri'),
    ('Dindigul', 'Dindigul'),
    ('Erode', 'Erode'),
    ('Kallakurichi', 'Kallakurichi'),
    ('Kancheepuram', 'Kancheepuram'),
    ('Kanyakumari', 'Kanyakumari'),
    ('Karur', 'Karur'),
    ('Krishnagiri', 'Krishnagiri'),
    ('Madurai', 'Madurai'),
    ('Mayiladuthurai', 'Mayiladuthurai'),
    ('Nagapattinam', 'Nagapattinam'),
    ('Namakkal', 'Namakkal'),
    ('Nilgiris', 'Nilgiris'),
    ('Perambalur', 'Perambalur'),
    ('Pudukkottai', 'Pudukkottai'),
    ('Ramanathapuram', 'Ramanathapuram'),
    ('Ranipet', 'Ranipet'),
    ('Salem', 'Salem'),
    ('Sivaganga', 'Sivaganga'),
    ('Tenkasi', 'Tenkasi'),
    ('Thanjavur', 'Thanjavur'),
    ('Theni', 'Theni'),
    ('Thoothukudi', 'Thoothukudi'),
    ('Tiruchirappalli', 'Tiruchirappalli'),
    ('Tirunelveli', 'Tirunelveli'),
    ('Tirupattur', 'Tirupattur'),
    ('Tiruppur', 'Tiruppur'),
    ('Tiruvallur', 'Tiruvallur'),
    ('Tiruvannamalai', 'Tiruvannamalai'),
    ('Tiruvarur', 'Tiruvarur'),
    ('Vellore', 'Vellore'),
    ('Viluppuram', 'Viluppuram'),
    ('Virudhunagar', 'Virudhunagar'),
]

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    district = forms.ChoiceField(
        choices=TN_DISTRICTS,
        widget=forms.Select(attrs={'onchange': 'loadTaluks()', 'class': 'form-control'})
    )
    taluk = forms.CharField(max_length=100)
    village = forms.CharField(max_length=100)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number',
                  'district', 'taluk', 'village',
                  'password1', 'password2', 'captcha']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()