from django.contrib import admin
from django.urls import path
from shop.views import shop
from shop import views

urlpatterns = [
    path('shop/', shop.as_view(),name="shop"),
    path('add_to_cart/<id>', views.add_to_cart,name="add_to_cart"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('remove_cart/<id>/', views.remove_cart,name = "remove_cart"),
    path('cart/', views.cart_view, name='cart'),
    # path('checkout/', views.checkout_view, name='checkout'),
    # path('checkout/success/', views.checkout_success, name='checkout_success'),
]
