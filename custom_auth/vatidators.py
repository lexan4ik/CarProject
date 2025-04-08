import re

from django import forms

def re_password(password):
    pattern = (r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*]).{10,}$')
    if not re.fullmatch(pattern, password, re.VERBOSE):
        raise forms.ValidationError('Длинна пароля должна быть больше 10 символов, должен содержать хотя бы одну цифру, букву в ниж. регистре, букву в верхнем регистре, один спец. символ\n')

def pass_validator(password):
    if not len(password) >= 10:
        raise forms.ValidationError('Длинна пароля должна быть больше 10 символов')


def search_number(password):
    for i in password:
        if i.isdigit():
            return True
    raise forms.ValidationError('Пароль должен содержать хотябы одну цифру')

def lower_word(password):
    for i in password:
        if i.islower():
            return True
    raise forms.ValidationError('Пароль должен содержать хотябы одну букву в нижнем регистре')

def upper_word(password):
    for i in password:
        if i.isupper():
            return True
    raise forms.ValidationError('Пароль должен содержать хотябы одну букву в верхнем регистре')

def spec_word(password):
    spec = ['!', '@', '#', '$', '%']
    for i in password:
        if i in spec:
            return True
    raise forms.ValidationError('Пароль должен содержать хотябы один спец. символ')

def custom_password_validator(password):
    pass_validator(password)
    search_number(password)
    lower_word(password)
    upper_word(password)
    spec_word(password)