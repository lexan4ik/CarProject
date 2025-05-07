from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from main.models import Car

@receiver(post_save, sender=Car)
def send_welcome_email(sender, instance, created, **kwargs): # Если пользователь только что создан
        send_mail(
            'Привет Никита!',
            'Ваша машина успешно добавлена!',
            f'{EMAIL_HOST_USER}',
            ['glushnevich@inbox.ru'],
            fail_silently=False,
        )

@receiver([post_delete, post_save], sender=Car, dispatch_uid='delete_cache')
def delete_cache_page(sender, **kwargs):
    cache.delete('main_page')
    print(sender)
    print(kwargs)