from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages  # Import messages
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import *
from .forms import *

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
        user.save() # Lưu user vào database
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
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_man.html',context)

def product_woman(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_woman.html',context)

def product_kid(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_kid.html',context)

def bestseller(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/bestseller.html',context)

def accessories(request):
    context = {}
    return render(request, 'app/accessories.html',context)

def aboutUs(request):
    context = {}
    return render(request, 'app/aboutUs.html',context)

def product_protect(request):
    context = {}
    return render(request, 'app/product_protect.html',context)

def socks(request):
    context = {}
    return render(request, 'app/socks.html',context)

def wallet(request):
    context = {}
    return render(request, 'app/wallet.html',context)


@login_required
def yourorder(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    context = {'orders': orders}
    return render(request, 'app/yourorder.html', context)

def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.all()
    colors = Color.objects.all()
    customer_id = request.user.customer.id  # Lấy customer_id từ request.user
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'customer_id': customer_id
    }
    return render(request, 'app/detail_product.html', context)

########################### view cho admin #########################

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
        return redirect('admin_product_list')
    context = {'product': product}
    return render(request, 'admin/admin_product_delete.html', context)

@login_required
def admin_product_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'admin/admin_product_list.html', context)

@login_required
def admin_product_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {'order': order}
    return render(request, 'admin/admin_product_detail.html', context)

@login_required
def admin_product_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = OrderForm(instance=order)
    context = {'form': form, 'order': order}
    return render(request, 'admin/admin_product_update.html', context)