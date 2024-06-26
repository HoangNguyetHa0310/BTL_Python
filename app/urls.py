from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/<int:customer_id>/', views.cart, name='cart'),
    path('payProduct/<int:pk>', views.payProduct, name="payProduct"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('checkout/', views.checkout, name="checkout"),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('product_woman/', views.product_woman, name="product_woman"),
    path('product_man/', views.product_man, name="product_man"),
    path('product_kid/', views.product_kid, name="product_kid"),
    path('bestseller/', views.bestseller, name="bestseller"),
    path('accessories/', views.accessories, name="accessories"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('detail_product/<int:pk>/', views.detail_product, name="detail_product"),
    path('product_protect/', views.product_protect, name="product_protect"),
    path('socks/', views.socks, name="socks"),
    path('wallet/', views.wallet, name="wallet"),
    path('yourorder/', views.yourorder, name="yourorder"),
    path('add_to_cart/<int:product_id>/<int:customer_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_cart_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('get_products/', views.get_products, name='get_products'),

    ###################### admin ###################
    path('dashboard/', views.dashboard, name='dashboard'),

    # Product
    path('admin_product_list/', views.admin_product_list, name='admin_product_list'),
    path('admin_product_create/', views.admin_product_create, name='admin_product_create'),
    path('admin_product_detail/<int:pk>/', views.admin_product_detail, name='admin_product_detail'),
    path('admin_product_update/<int:pk>/', views.admin_product_update, name='admin_product_update'),
    path('admin_product_delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),

    # Category
    path('admin_category_list/', views.admin_category_list, name='admin_category_list'),
    path('admin_category_create/', views.admin_category_create, name='admin_category_create'),
    path('admin_category_detail/<int:category_id>/', views.admin_category_detail, name='admin_category_detail'),
    path('admin_category_update/<int:category_id>/', views.admin_category_update, name='admin_category_update'),
    path('admin_category_delete/<int:category_id>/', views.admin_category_delete, name='admin_category_delete'),

    # Brand
    path('admin_brand_list/', views.admin_brand_list, name='admin_brand_list'),
    path('admin_brand_create/', views.admin_brand_create, name='admin_brand_create'),
    path('admin_brand_detail/<int:brand_id>/', views.admin_brand_detail, name='admin_brand_detail'),
    path('admin_brand_update/<int:brand_id>/', views.admin_brand_update, name='admin_brand_update'),
    path('admin_brand_delete/<int:brand_id>/', views.admin_brand_delete, name='admin_brand_delete'),

    # Order
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('admin_order_detail/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin_update_order_status/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),

    # User
    path('admin_user_management/', views.admin_user_management, name='admin_user_management'),
]