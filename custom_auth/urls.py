from tkinter.font import names

from django.urls import path

from custom_auth.views import registration, user_login, user_logout

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]