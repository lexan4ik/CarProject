from django.urls import path

from custom_auth.views import registration

urlpatterns = [
    path('registration/', registration, name='registration')
]