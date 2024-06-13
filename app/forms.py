from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount', 'image', 'category', 'brand', 'stock', 'active', 'size',
                  'color']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'total_price', 'shipping_address', 'payment_method', 'tracking_number']
