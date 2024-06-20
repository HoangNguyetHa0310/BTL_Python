from django.contrib.auth.decorators import *
from django.shortcuts import *
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q


def index(request):
    return render(request, 'app/index.html')

def cartItem(request):
    # size_id = request.POST.get('size')
    # color_id = request.POST.get('color')
    # size = get_object_or_404(Size, id=size_id)
    # color = get_object_or_404(Color, id=color_id)
    
    context = {
            # 'size': size,
            # 'color': color,
        }
    return render(request, 'app/cartItem.html', context)

def cartItem1(request,pk):
    product = Product.objects.get(pk=pk)
    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    size = get_object_or_404(Size, id=size_id)
    color = get_object_or_404(Color, id=color_id)
    context = {
        'size': size,
        'color': color,
        'product':product,
    }
    return render(request, 'app/cartItem.html', context)

def payProduct(request):
    context = {}
    return render(request, 'app/payProduct.html',context)


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


def checkout(request):
    context = {}
    return render(request, 'app/checkout.html',context)
# (THÊM PHẦN DƯỚI NÀY VÀO THÔI NGÀY 20/2/2024 )
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

    # Lọc sản phẩm
    products = Product.objects.all()
    if selected_size:
        products = products.filter(size_id=selected_size)
    if selected_price:
        products = products.filter(price=selected_price)
    if selected_color:
        products = products.filter(color_id=selected_color)
    if selected_brand:
        products = products.filter(brand_id=selected_brand)

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
    }
    return render(request, 'app/product_man.html', context)

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


def yourorder(request):
    context = {}
    return render(request, 'app/yourorder.html',context)

def detail_product(request):
    # products = get_object_or_404(Product,id=pk)
    # context = {'product': product}
    # products = Product.objects.get(id=pk)
    sizes = Size.objects.all()
    colors = Color.objects.all()
    context = {
        'sizes': sizes,
        'colors' : colors,
        # 'products':products,
    }
    return render(request, 'app/detail_product.html', context)

def detail_product1(request,pk):
    products = Product.objects.get(id=pk)
    sizes = Size.objects.all()
    colors = Color.objects.all()
    context ={
        'products':products,
        'sizes': sizes,
        'colors' : colors,
    }
    return render(request, 'app/detail_product.html', context)



########################### view cho admin #########################

# @login_required
# def admin_product_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'admin/admin_product_list.html', context)

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
    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=products)
    context = {'form': form, 'product': products}
    return render(request, 'admin/admin_product_update.html', context)

@login_required
def admin_product_delete(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        products.delete()
        return redirect('admin_product_list')
    context = {'product': products}
    return render(request, 'admin/admin_product_delete.html', context)

@login_required
def admin_product_list(request):
    products = Product.objects.all()
    context = {'product': products}
    return render(request, 'admin/admin_product_list.html', context)

@login_required
def admin_product_detail(request, pk):
    products = get_object_or_404(Product, pk=pk)
    context = {'product': products}
    return render(request, 'admin/admin_product_detail.html', context)

@login_required
def admin_product_update(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=products)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = OrderForm(instance=products)
    context = {'form': form, 'order': products}
    return render(request, 'admin/admin_product_update.html', context)