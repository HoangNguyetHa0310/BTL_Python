from django.contrib import admin
from django.contrib import admin
from .models import (
    Category,
    Brand,
    Attribute,
    AttributeValue,
    Product,
    ProductAttribute,
    Customer,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Size,
    Color
)

# ------------------------------ Danh mục sản phẩm ------------------------------ #
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ------------------------------ Thương hiệu ------------------------------ #
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


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
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand', 'stock', 'active', 'date_added', 'get_sizes', 'get_colors')
    list_filter = ('category', 'brand', 'active')
    search_fields = ('name', 'description')
    inlines = [ProductAttributeInline]

    def get_sizes(self, obj):
        return ", ".join([str(size) for size in obj.size.all()])
    get_sizes.short_description = 'Sizes'

    def get_colors(self, obj):
        return ", ".join([str(color) for color in obj.color.all()])
    get_colors.short_description = 'Colors'


# ------------------------------ Khách hàng ------------------------------ #
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'city', 'country')


# ------------------------------ Giỏ hàng ------------------------------ #

class cartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'get_cart_items_summary')
    readonly_fields = ('get_cart_items_summary',)  # Ensure it's read-only

    def get_cart_items_summary(self, obj):
        """Returns a summary of items in the cart."""
        cart_items = obj.cartitem_set.all()
        summary = []
        for item in cart_items:
            summary.append(
                f"{item.quantity} x {item.product.name} - Size: {item.size} - Color: {item.color}"
            )
        return "<br>".join(summary)  # Join items with line breaks
    get_cart_items_summary.short_description = 'Cart Items'
    get_cart_items_summary.allow_tags = True  # Allow HTML in the summary

admin.site.register(Cart, cartAdmin)


# ------------------------------ Đơn hàng ------------------------------ #
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer', 'order_date', 'status', 'total_price', 'shipping_address', 'payment_method', 'tracking_number')
    list_filter = ('status',)
    list_editable = ('status',)
    readonly_fields = ('order_date',)


# ------------------------------ Chi tiết đơn hàng ------------------------------ #
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'size', 'color')


# ------------------------------ Size ------------------------------ #
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


# ------------------------------ Màu sắc ------------------------------ #
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')