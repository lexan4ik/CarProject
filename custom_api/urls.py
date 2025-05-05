from django.urls import path

from custom_api.views import get_all_car, get_all_image, search_cars

# from custom_api.views import ProductList, ProductDetail

urlpatterns = [
    # path('car/', ProductList.as_view(), name='car-list'),
    # path('car/<int:pk>/', ProductDetail.as_view(), name='car-detail'),
    path('cars/', get_all_car, name='api_cars'),
    path('images/', get_all_image),
    path('search_cars/', search_cars),


]