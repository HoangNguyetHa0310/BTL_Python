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

    # Thêm trường size và color
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)

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
class CartItem(models.Model):
    """
    Mô hình giỏ hàng.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.user.username} - {self.product.name} x {self.quantity}"

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

    def __str__(self):
        return f"Order #{self.id}"

# ------------------------------ Chi tiết đơn hàng ------------------------------ #
class OrderItem(models.Model):
    """
    Mô hình chi tiết đơn hàng.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order} - {self.product.name} x {self.quantity}"