from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('cartItem/', views.cartItem, name="cartItem"),
    path('cartItem1/<int:pk>', views.cartItem1, name="cartItem1"),
    path('payProduct/', views.payProduct, name="payProduct"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('checkout/', views.checkout, name="checkout"),
    path('product_woman/', views.product_woman, name="product_woman"),
    path('product_man/', views.product_man, name="product_man"),
    path('product_kid/', views.product_kid, name="product_kid"),
    path('bestseller/', views.bestseller, name="bestseller"),
    path('accessories/', views.accessories, name="accessories"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('detail_product1/<int:pk>/', views.detail_product1, name="detail_product1"),
    path('detail_product/', views.detail_product, name="detail_product"),
    path('product_protect/', views.product_protect, name="product_protect"),
    path('socks/', views.socks, name="socks"),
    path('wallet/', views.wallet, name="wallet"),
    path('yourorder/', views.yourorder, name="yourorder"),
    
    

    
    ###################### admin ###################
    path('admin_product_create/', views.admin_product_create, name="admin_product_create"),
    path('admin_product_delete/', views.admin_product_delete, name="admin_product_delete"),
    path('admin_product_detail/', views.admin_product_detail, name="admin_product_detail"),
    path('admin_product_list/', views.admin_product_list, name="admin_product_list"),
    path('admin_product_update/', views.admin_product_update, name="admin_product_update"),

]

