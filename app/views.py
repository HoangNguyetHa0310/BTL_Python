from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages  # Import messages

from .models import *
from .forms import *

def index(request):
    return render(request, 'app/index.html')

def cartItem(request,pk):
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

def payProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    selected_size = request.session.get('selected_size')
    selected_color = request.session.get('selected_color')
    context = {'product': product, 'selected_size': selected_size, 'selected_color': selected_color}
    return render(request, 'app/payProduct.html', context)

def login(request):
    context = {}
    return render(request, 'app/login.html',context)

def register(request):
    context = {}
    return render(request, 'app/register.html',context)

def checkout(request):
    context = {}
    return render(request, 'app/checkout.html',context)

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


def yourorder(request):
    context = {}
    return render(request, 'app/yourorder.html',context)

def detail_product(request,pk):
    product = Product.objects.get(pk=pk)
    sizes = Size.objects.all()
    colors = Color.objects.all()
    context ={
        'product':product,
        'sizes': sizes,
        'colors' : colors,
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