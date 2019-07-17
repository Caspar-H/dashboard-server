from django.shortcuts import render, redirect
from .import models
from .import forms
# import hashlib


# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        return redirect('/home/')

    if request.method == 'POST':
        login_forms = forms.UserForm(request.POST)
        message = "Password cannot be empty"

        if login_forms.is_valid():
            username = login_forms.cleaned_data.get('username')
            password = login_forms.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = "User not existing"
                return render(request, 'login/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/home/')
            else:
                message = "Wrong password, please try again"
                return render(request, 'login/login.html', locals())

        else:
            return render(request, 'login/login.html', locals())
    login_forms = forms.UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/logout/')


def register(request):
    if request.session.get('is_login', None):
        return redirect('/home/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = 'Please check the content'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            team = register_form.cleaned_data.get('team')

            if password1 != password2:
                message = 'Password does not match'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'Username has already been used'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'Email has been used'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.team = team
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals)
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())
