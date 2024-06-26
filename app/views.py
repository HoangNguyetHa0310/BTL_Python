from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages  # Import messages
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.http import JsonResponse
import unicodedata
from django.db.models import Case, When, F, BooleanField
from django.db.models import Count
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear, TruncDay

def index(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            messages.warning(request, "You need to create a customer profile to continue.")
            return redirect('create_customer_profile')  # Replace with your URL
    else:
        customer = None
    context = {'customer': customer}
    return render(request, 'app/index.html', context)


@login_required
def cart(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    try:
        cart = Cart.objects.get(customer=customer)
        cart_items = cart.get_cart_items()
        total_price = cart.get_total_price()
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'app/cart.html', context)


@login_required
def add_to_cart(request, product_id, customer_id):
    product = get_object_or_404(Product, pk=product_id)
    customer = get_object_or_404(Customer, pk=customer_id)

    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    size = get_object_or_404(Size, id=size_id) if size_id else None
    color = get_object_or_404(Color, id=color_id) if color_id else None

    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Sản phẩm {product.name} đã được thêm vào giỏ hàng")
    return redirect('cart', customer_id=customer_id)


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        # Get customer_id from the cart item
        customer_id = cart_item.cart.customer.id
        return redirect('cart', customer_id=customer_id)
    return redirect('cart')


@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    customer_id = cart_item.cart.customer.id
    cart_item.delete()
    return redirect('cart', customer_id=customer_id)


def payProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    selected_size = request.session.get('selected_size')
    selected_color = request.session.get('selected_color')
    context = {'product': product, 'selected_size': selected_size, 'selected_color': selected_color}
    return render(request, 'app/payProduct.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')

        # Kiểm tra xem email đã tồn tại hay chưa
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại. Vui lòng chọn email khác.')
            return render(request, 'app/register.html', {})

        # Tạo user mới
        user = User.objects.create_user(
            username=email,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Lưu thông tin khách hàng
        user.save()  # Lưu user vào database
        customer = Customer.objects.create(
            user=user,
            phone=phone,
            address=address,
            city=city,
            country=country,
        )
        # Đăng nhập user tự động sau khi tạo tài khoản
        user = authenticate(username=email, password=password)
        if user is not None:
            # Đăng nhập user vào hệ thống
            messages.success(request, 'Tạo tài khoản thành công!')
            return redirect('login')
        else:
            messages.error(request, 'Lỗi tạo tài khoản.')
            return render(request, 'app/register.html', {})

    else:
        context = {}
        return render(request, 'app/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return redirect('index')  # Chuyển hướng đến trang index
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')
            return render(request, 'app/login.html', {})

    else:
        context = {}
        return render(request, 'app/login.html', context)


@login_required
def checkout(request):
    customer = request.user.customer
    cart = None
    cart_items = []
    total_price = 0

    try:
        cart = Cart.objects.get(customer=customer)
        cart_items = cart.get_cart_items()
        total_price = cart.get_total_price()
    except Cart.DoesNotExist:
        pass

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.total_price = total_price
            # Lưu trữ phương thức thanh toán vào order
            order.payment_method = request.POST.get('payment_method')
            order.save()

            for cart_item in cart_items:
                order.items.add(cart_item)
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    size=cart_item.size,
                    color=cart_item.color,
                )

            if cart:  # Only delete the cart if it exists
                cart.delete()

            messages.success(request, "Đơn hàng của bạn đã được đặt thành công! Cảm ơn bạn.")
            # Chuyển hướng đến trang xác nhận đơn hàng
            return redirect('order_confirmation', order_id=order.pk)
    else:
        form = OrderForm(initial={'customer': customer})

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
        'customer': customer
    }
    return render(request, 'app/checkout.html', context)


# Trang xác nhận đơn hàng
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {'order': order, 'order_items': order.items.all()}
    return render(request, 'app/order_confirmation.html', context)


def product_man(request):
    sizes = Size.objects.all()
    prices = Product.objects.values_list('price', flat=True).distinct()
    colors = Color.objects.all()
    brands = Brand.objects.all()

    # Lấy dữ liệu từ request
    selected_size = request.GET.get('size')
    selected_price = request.GET.get('price')
    selected_color = request.GET.get('color')
    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort')  # Lấy giá trị sort
    q = request.GET.get('q')


    # Lọc sản phẩm
    products = Product.objects.all()
    if selected_size:
        products = products.filter(size=selected_size)
    if selected_price:
        products = products.filter(price=selected_price)
    if selected_color:
        products = products.filter(color=selected_color)
    if selected_brand:
        products = products.filter(brand=selected_brand)
    if q:
        # q_normalized = unicodedata.normalize('NFKD', q).encode('ascii', 'ignore').decode('ascii').lower()
        # products = products.filter(
        #     # Kiểm tra xem name có chứa bất kỳ ký tự nào trong q hay không
        #     name__iregex=r'.*[' + q_normalized + r'].*'
        # )
        products = products.filter(name__icontains=q)

        # Sắp xếp sản phẩm
    if sort_by == 'ascending':
        products = products.order_by('name')  # Sắp xếp theo tên A-Z
    elif sort_by == 'descending':
        products = products.order_by('-name')  # Sắp xếp theo tên Z-A

    context = {
        'products': products,
        'sizes': sizes,
        'prices': prices,
        'colors': colors,
        'brands': brands,
        'selected_size': selected_size,
        'selected_price': selected_price,
        'selected_color': selected_color,
        'selected_brand': selected_brand,
        'sort_by': sort_by,  # Truyền giá trị sort_by vào template
        'search_term': q,

    }
    return render(request, 'app/product_man.html', context)


def product_woman(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_woman.html', context)


def product_kid(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_kid.html', context)


# def bestseller(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'app/bestseller.html', context)
def bestseller(request):
    # Sử dụng .annotate để thêm trường tính toán
    hot_products = Product.objects.annotate(
        is_low_stock=Case(
            When(stock__lte=F('stock') * 0.5, then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).filter(is_low_stock=True).order_by('-date_added')
    context = {'hot_products': hot_products}
    return render(request, 'app/bestseller.html', context)

def accessories(request):
    context = {}
    return render(request, 'app/accessories.html', context)


def aboutUs(request):
    context = {}
    return render(request, 'app/aboutUs.html', context)


def product_protect(request):
    context = {}
    return render(request, 'app/product_protect.html', context)


def socks(request):
    context = {}
    return render(request, 'app/socks.html', context)


def wallet(request):
    context = {}
    return render(request, 'app/wallet.html', context)


@login_required
def yourorder(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    context = {'orders': orders}
    return render(request, 'app/yourorder.html', context)


from django.shortcuts import render, get_object_or_404

def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.user.is_authenticated:
        customer_id = request.user.customer.id
    else:
        customer_id = None

    # Lấy sản phẩm gợi ý (ví dụ: cùng loại)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        pk=product.pk
    )[:9]  # Lấy tối đa 9 sản phẩm

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'customer_id': customer_id,
        'related_products': related_products,
    }
    return render(request, 'app/detail_product.html', context)

def get_products(request):
    products = Product.objects.all()
    product_data = [{'name': p.name, 'id': p.id} for p in products]  # Thêm ID sản phẩm
    return JsonResponse(product_data, safe=False)


########################### view cho admin #########################
@login_required
def dashboard(request):
    today = datetime.now().date()
    last_month = today - timedelta(days=30)

    revenue_by_day = Order.objects.annotate(day=TruncDay('order_date')).values('day').annotate(
        total=Sum('total_price')).order_by('day')
    revenue_by_month = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
        total=Sum('total_price')).order_by('month')
    revenue_by_year = Order.objects.annotate(year=TruncYear('order_date')).values('year').annotate(
        total=Sum('total_price')).order_by('year')

    total_orders_this_month = Order.objects.filter(order_date__month=today.month).count()
    total_revenue_this_month = Order.objects.filter(order_date__month=today.month).aggregate(sum=Sum('total_price'))['sum'] or 0
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()

    top_selling_products = Product.objects.annotate(
        total_sold=Count('orderitem', filter=Q(orderitem__order__order_date__gte=last_month))
    ).order_by('-total_sold')[:5]

    recent_order_items = OrderItem.objects.select_related(
        'order', 'product', 'size', 'color'
    ).filter(order__order_date__month=today.month)

    context = {
        'total_orders_this_month': total_orders_this_month,
        'total_revenue_this_month': total_revenue_this_month,
        'total_products': total_products,
        'total_customers': total_customers,
        'top_selling_products': top_selling_products,
        'recent_order_items': recent_order_items,
        'revenue_by_day': revenue_by_day,
        'revenue_by_month': revenue_by_month,
        'revenue_by_year': revenue_by_year,
    }
    return render(request, 'admin/dashboard.html', context)

#----------------------- Admin Product Views ------------------------------#

@login_required
def admin_product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'admin/admin_product_list.html', context)

@login_required
def admin_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'admin/admin_product_detail.html', context)

@login_required
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sản phẩm đã được tạo thành công!")
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'admin/admin_product_create.html', context)

@login_required
def admin_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Sản phẩm đã được cập nhật thành công!")
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    context = {'form': form, 'product': product}
    return render(request, 'admin/admin_product_update.html', context)

@login_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Sản phẩm đã bị xóa!")
        return redirect('admin_product_list')
    context = {'product': product}
    return render(request, 'admin/admin_product_delete.html', context)


#----------------------- Admin Category Views ------------------------------#

@login_required
def admin_category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'admin/admin_category_list.html', context)

@login_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Danh mục đã được tạo thành công!")
            return redirect('admin_category_list')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'admin/admin_category_create.html', context)

@login_required
def admin_category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}
    return render(request, 'admin/admin_category_detail.html', context)

@login_required
def admin_category_update(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Danh mục đã được cập nhật thành công!")
            return redirect('admin_category_list')
    else:
        form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'admin/admin_category_update.html', context)

@login_required
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Danh mục đã bị xóa!")
        return redirect('admin_category_list')
    context = {'category': category}
    return render(request, 'admin/admin_category_delete.html', context)

#----------------------- Admin Brand Views ------------------------------#

@login_required
def admin_brand_list(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request, 'admin/admin_brand_list.html', context)

@login_required
def admin_brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Thương hiệu đã được tạo thành công!")
            return redirect('admin_brand_list')
    else:
        form = BrandForm()
    context = {'form': form}
    return render(request, 'admin/admin_brand_create.html', context)

@login_required
def admin_brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    context = {'brand': brand}
    return render(request, 'admin/admin_brand_detail.html', context)

@login_required
def admin_brand_update(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)  # Lấy đối tượng Brand

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Thương hiệu đã được cập nhật thành công!")
            return redirect('admin_brand_list')
    else:
        form = BrandForm(instance=brand)  # Khởi tạo form với dữ liệu của Brand

    # Dòng code cần sửa: Thêm 'brand': brand vào context
    context = {'form': form, 'brand': brand}
    return render(request, 'admin/admin_brand_update.html', context)

@login_required
def admin_brand_delete(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, "Thương hiệu đã bị xóa!")
        return redirect('admin_brand_list')
    context = {'brand': brand}
    return render(request, 'admin/admin_brand_delete.html', context)

#----------------------- Admin Order Views ------------------------------#

@login_required
def admin_order_list(request):
    orders = Order.objects.all()  # Lấy tất cả các đơn hàng
    context = {'orders': orders}
    return render(request, 'admin/admin_order_list.html', context)

@login_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.items.all()
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'admin/admin_order_detail.html', context)

@login_required
def admin_update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        messages.success(request, f"Trạng thái đơn hàng #{order_id} đã được cập nhật thành công!")

    return redirect('admin_order_list')

#----------------------- Admin User Views ------------------------------#

@login_required
def admin_user_management(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'admin/admin_user_management.html', context)