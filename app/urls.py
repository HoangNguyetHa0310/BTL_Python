from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base,name="base"),
    path('', views.index,name="index"),
    path('cart/', views.cart, name="cart"),
    path('login/', views.cart, name="login"),
    path('register/', views.cart, name="register"),
    path('product_woman/', views.product_woman, name="product_woman"),
    path('product_man/', views.product_man, name="product_man"),
    path('product_kid/', views.product_kid, name="product_kid"),
    path('bestseller/', views.new_product, name="bestseller"),
    path('accessories/', views.new_product, name="accessories"),
    path('aboutUs/', views.new_product, name="aboutUs"),
]

