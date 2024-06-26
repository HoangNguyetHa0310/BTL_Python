from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'payment_method']  # Add other fields as needed
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].choices = [
            ('COD', 'Thanh toán khi nhận hàng'),
            ('Momo', 'Momo'),
            ('VNPay', 'VNPay'),
        ]
        # Add any initial values to form fields
        if 'customer' in kwargs:
            customer = kwargs.pop('customer')
            self.initial['shipping_address'] = customer.address

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

