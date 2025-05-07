from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path, include

from custom_auth.views import registration, user_login, user_logout, change_pass,account

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('account/', account, name='account'),
    path('change_pass/', change_pass, name='change_pass'),
    path('reset_pass/', PasswordResetView.as_view(), name='reset_pass'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]