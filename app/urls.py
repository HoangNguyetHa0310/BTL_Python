from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base,name="base"),
    path('', views.index,name="index"),
    path('cart/', views.cart, name="cart"),
    path('product_woman/', views.product_woman, name="product_woman"),
    path('product_man/', views.product_man, name="product_man"),
    path('product_kid/', views.product_kid, name="product_kid"),
    path('new_product/', views.new_product, name="new_product"),
]

