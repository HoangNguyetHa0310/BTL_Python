from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('cart/', views.cart, name="cart"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('checkout/', views.checkout, name="checkout"),
    path('product_woman/', views.product_woman, name="product_woman"),
    path('product_man/', views.product_man, name="product_man"),
    path('product_kid/', views.product_kid, name="product_kid"),
    path('bestseller/', views.bestseller, name="bestseller"),
    path('accessories/', views.accessories, name="accessories"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('detail_product/', views.detail_product, name="detail_product"),

]

