from django.shortcuts import render
from django.http import HttpResponse
from .models import *



def index(request):
    return render(request, 'app/index.html')


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        item = []
    context = {'item':items,'order':order}
    return render(request, 'app/cart.html',context)

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

def detail_product(request):
    context = {}
    return render(request, 'app/detail_product.html',context)