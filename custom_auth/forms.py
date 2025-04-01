from django import forms
from django.contrib.auth.models import User

#Форма регистрации
class Registration(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User

        fields = ['username', 'password', 'confirm_password']


    def clean(self):
        cd = self.cleaned_data
        pass1 = cd.get('password')
        conf_pass = cd.get('confirm_password')
        if pass1 != conf_pass:
            raise forms.ValidationError('Пароли не совпадают!')
