from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from custom_auth.forms import Registration, LoginForm


# Create your views here.

# Обработка формы регистрации
def registration(request):

    form = Registration()


    print(request.POST)
    if request.method == 'POST':
        form = Registration(request.POST)
        print(form.non_field_errors())
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

    context = {
        'form': form,
    }

    return render(request, 'registration.html', context)

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                message_error = 'Не правильный логин или пароль!'
                form.add_error(None, message_error)

    context = {
        'form': form,
    }

    return render(request, 'user_login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect('main')