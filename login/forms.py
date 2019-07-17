from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''
    }))
    password = forms.CharField(label='Password', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    captcha = CaptchaField(label='captcha')


class RegisterForm(forms.Form):
    team_name = (
        ('Australian RF Team', 'AU RF'),
        ('Singapore RF Team', 'SG RF'),
        ('General Management', 'GM'),
    )

    username = forms.CharField(label='Username', max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(label='Password', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='Confirm Password', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    team = forms.ChoiceField(label='Team', choices=team_name)
    captcha = CaptchaField(label='captcha')


