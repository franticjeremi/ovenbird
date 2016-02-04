# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from captcha.fields import CaptchaField

from registration.models import CustomUser

class RegistrationForm(UserCreationForm):
    """A form for registration new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        required=True, 
        label="Повторный пароль", 
        widget=forms.PasswordInput
    )
    email = forms.EmailField(
        required=True, 
        label="Электронная почта", 
        widget=forms.TextInput(attrs={'placeholder': 'xxx@yourmail.ru','type':'email'})
    )
    captcha = CaptchaField(
        label="Капча"
    )

    class Meta:
        model = CustomUser
        fields = ['email','password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
            
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class MyAuthenticationForm(forms.Form):

    email = forms.EmailField(
        required=True, 
        label="Электронная почта", 
        widget=forms.TextInput
    )
    password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput
    )

    class Meta:
        fields = ['email','password']