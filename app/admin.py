from django.contrib import admin
from .models import (
    Category,
    Brand,
    Attribute,
    AttributeValue,
    Product,
    ProductAttribute,
    Customer,
    CartItem,
    Order,
    OrderItem,
)

# ------------------------------ Danh mục sản phẩm ------------------------------ #
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)

# ------------------------------ Thương hiệu ------------------------------ #
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ------------------------------ Thuộc tính sản phẩm ------------------------------ #
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ------------------------------ Giá trị thuộc tính ------------------------------ #
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)

# ------------------------------ Sản phẩm ------------------------------ #
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'category', 'brand', 'stock', 'active')
    list_filter = ('category', 'brand', 'active')
    search_fields = ('name',)
    list_editable = ('price', 'discount', 'stock', 'active')

# ------------------------------ Sản phẩm - Thuộc tính ------------------------------ #
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute_value')

# ------------------------------ Khách hàng ------------------------------ #
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'city', 'country')

# ------------------------------ Giỏ hàng ------------------------------ #
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')

# ------------------------------ Đơn hàng ------------------------------ #
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'status', 'total_price', 'shipping_address', 'payment_method', 'tracking_number')
    list_filter = ('status',)
    list_editable = ('status',)
    readonly_fields = ('order_date',)

# ------------------------------ Chi tiết đơn hàng ------------------------------ #
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')