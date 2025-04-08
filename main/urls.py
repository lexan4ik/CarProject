from django.urls import path

from .views import (get_main_page, add_car, detail,
                    edit_car, edit_car_new, catalog,
                    brands, themes, current_theme)

urlpatterns = [
    path('', get_main_page, name='main'),
    path('add_car/', add_car, name='add_car'),
    path('detail/<int:id>/', detail, name='detail'),
    path('edit_car/<int:id>/', edit_car, name='edit_car'),
    path('edit_car_new/<int:id>/', edit_car_new, name='edit_car_new'),
    path('catalogcatalog/', catalog, name='catalog'),
    path('brands/', brands, name='brands'),
    path('themes', themes),
    path('/', current_theme, name='current_theme'),
]