from django.db import models
from django.contrib.auth.models import User

# ------------------------------ Danh mục sản phẩm ------------------------------ #
class Category(models.Model):
    """
    Mô hình danh mục sản phẩm.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='children')

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def ImageUrl(self):
        try:
            return self.image.url
        except:
            return ''

# ------------------------------ Thương hiệu ------------------------------ #
class Brand(models.Model):
    """
    Mô hình thương hiệu.
    """
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brand_logos', blank=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def LogoUrl(self):
        try:
            return self.logo.url
        except:
            return ''

# ------------------------------ Thuộc tính sản phẩm ------------------------------ #
class Attribute(models.Model):
    """
    Mô hình thuộc tính sản phẩm.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ------------------------------ Giá trị thuộc tính ------------------------------ #
class AttributeValue(models.Model):
    """
    Mô hình giá trị thuộc tính.
    """
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

# ------------------------------ Size ------------------------------ #
class Size(models.Model):
    """
    Mô hình size sản phẩm.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# ------------------------------ Màu sắc ------------------------------ #
class Color(models.Model):
    """
    Mô hình màu sắc sản phẩm.
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7, blank=True)  # Mã màu (ví dụ: #FFFFFF)

    def __str__(self):
        return self.name

# ------------------------------ Sản phẩm ------------------------------ #
class Product(models.Model):
    """
    Mô hình sản phẩm.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # Sử dụng ManyToManyField cho size và color
    size = models.ManyToManyField(Size, blank=True)
    color = models.ManyToManyField(Color, blank=True)

    class Meta:
        ordering = ['-date_added']  # Sắp xếp sản phẩm theo ngày thêm mới nhất

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        return self.price - (self.price * (self.discount / 100))

    @property
    def ImageUrl(self):
        try:
            return self.image.url
        except:
            return ''

    # Lấy các thuộc tính sản phẩm
    def get_attributes(self):
        return self.productattribute_set.all()

    # @property
    # def is_low_stock(self):
    #     """
    #     Kiểm tra xem sản phẩm có tồn kho thấp hay không (dưới 50% lượng tồn kho)
    #     """
    #     return self.stock <= (self.stock * 0.5)
# ------------------------------ Sản phẩm - Thuộc tính ------------------------------ #
class ProductAttribute(models.Model):
    """
    Mô hình liên kết giữa sản phẩm và giá trị thuộc tính.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"

# ------------------------------ Khách hàng ------------------------------ #
class Customer(models.Model):
    """
    Mô hình khách hàng.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"

# ------------------------------ Giỏ hàng ------------------------------ #
class Cart(models.Model):
    """
    Mô hình giỏ hàng.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.customer.user.username}"

    def get_cart_items(self):
        return self.cartitem_set.all()

    def get_total_price(self):
        total = 0
        for item in self.get_cart_items():
            total += item.product.price * item.quantity
        return total

class CartItem(models.Model):
    """
    Mô hình chi tiết giỏ hàng.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Size: {self.size} - Color: {self.color}"

# ------------------------------ Đơn hàng ------------------------------ #
class Order(models.Model):
    """
    Mô hình đơn hàng.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Chờ xử lý", choices=[
        ('Chờ xử lý', 'Chờ xử lý'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đang giao hàng', 'Đang giao hàng'),
        ('Hoàn thành', 'Hoàn thành'),
        ('Hủy đơn', 'Hủy đơn'),
    ])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50, blank=True)
    items = models.ManyToManyField(CartItem)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

    def save(self, *args, **kwargs):
        """
        Override save() để cập nhật trạng thái is_low_stock của sản phẩm
        """
        super().save(*args, **kwargs)

        # Cập nhật trạng thái is_low_stock cho từng sản phẩm trong đơn hàng
        for order_item in self.orderitem_set.all():
            if order_item.quantity > (order_item.product.stock * 0.5):
                order_item.product.is_low_stock = True
            else:
                order_item.product.is_low_stock = False
            order_item.product.save()

# ------------------------------ Chi tiết đơn hàng ------------------------------ #

class OrderItem(models.Model):
    """
    Mô hình chi tiết đơn hàng.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.order} - {self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        """
        Override save() để cập nhật trạng thái is_low_stock của sản phẩm
        """
        super().save(*args, **kwargs)

        # Kiểm tra xem OrderItem.quantity có lớn hơn 50% stock của Product không
        if self.quantity > (self.product.stock * 0.5):
            # Cập nhật trạng thái is_low_stock của Product
            self.product.is_low_stock = True
            self.product.save()

    # def save(self, *args, **kwargs):
    #     """
    #     Override save() để cập nhật trạng thái is_low_stock của sản phẩm
    #     """
    #     super().save(*args, **kwargs)
    #
    #     # Kiểm tra xem OrderItem.quantity có lớn hơn 50% stock của Product không
    #     if self.quantity > (self.product.stock * 0.5):
    #         # Cập nhật trạng thái is_low_stock của Product
    #         self.product.is_low_stock = True
    #         self.product.save()


