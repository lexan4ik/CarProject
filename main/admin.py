from django.contrib import admin

from main.models import Car, Brand, ImageCar, Color, Model

# Register your models here.

admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(ImageCar)
admin.site.register(Color)
admin.site.register(Model)
