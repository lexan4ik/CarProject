from django import forms
from django.contrib.auth.models import User

from custom_auth.vatidators import custom_password_validator, re_password


#Форма регистрации
class Registration(forms.ModelForm):

    confirm_password = forms.CharField(label='Повторите пароль',widget=forms.PasswordInput, validators=[re_password])

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[re_password])

    class Meta:
        model = User

        fields = ['username', 'email', 'password', 'confirm_password']

        labels = {'email': 'Майл', 'username': 'Логин',}

        help_texts = {'username': ''}



    def clean(self):
        cd = self.cleaned_data
        pass1 = cd.get('password')
        conf_pass = cd.get('confirm_password')
        if pass1 != conf_pass:
            raise forms.ValidationError('Пароли не совпадают!')

class LoginForm(forms.Form):

    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput)


class ChangePassword(forms.Form):

    old_password = forms.CharField(label='Введите старый пароль',widget=forms.PasswordInput)
    password = forms.CharField(label='Введите новый пароль', widget=forms.PasswordInput)

