from django.urls import path

from cart.views import cart, cart_add, cart_remove

urlpatterns = [
    path('', cart, name='cart'),
    path('cart_add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart_remove/<int:product_id>/', cart_remove, name='cart_remove'),
]