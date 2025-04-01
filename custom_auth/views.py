from django.contrib.auth.models import User
from django.shortcuts import render

from custom_auth.forms import Registration


# Create your views here.

# Обработка формы регистрации
def registration(request):

    form = Registration()
    context = {
        'form': form,
    }
    print(request.POST)
    if request.method == 'POST':
        form = Registration(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()



    return render(request, 'registration.html', context)
