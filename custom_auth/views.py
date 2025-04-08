from django.contrib import auth
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from custom_auth.forms import Registration, LoginForm, ChangePassword


# Create your views here.

# Обработка личного кабинета
def account(request):

    return render(request, 'account.html')

# Обработка восстановления пароля
def reset_pass(request):
    pass
# Обработка смены пароля
def change_pass(request):

    form = ChangePassword()

    if request.method == 'POST':
        form = ChangePassword(request.POST)
        print(request.POST)
        print(request.user)
        if form.is_valid():
            print(form.cleaned_data)
            if check_password(form.cleaned_data.get('old_password'), request.user.password):
                user = User.objects.get(username=request.user.username)
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                update_session_auth_hash(request, user)
            else:
                form.add_error(None,'Старый пароль введен неверно!')
        else:
            form.add_error(None, 'Форма заполнена некорректно!')
    context = {
        'form': form,
    }

    return render(request, 'change_pass.html', context=context)

# Обработка формы регистрации
def registration(request):

    form = Registration()

# 1 спец. 10 символов, 1 заглавную, 1 строчную и 1 цифру
    print(request.POST)
    if request.method == 'POST':
        form = Registration(request.POST)
        print(form.non_field_errors())
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            return redirect('user_login')

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