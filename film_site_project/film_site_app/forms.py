from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    # Робимо email необов'язковим для заповнення у формі
    email = forms.EmailField(required=False, label="Електронна пошта")

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # Робимо телефон та аватарку чітко необов'язковими для форми
    phone = forms.CharField(required=False, label="Номер телефону")
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'phone']