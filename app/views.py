from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return render(request, 'app/index.html')


def cart(request):
    context = {}
    return render(request, 'app/cart.html',context)


def checkout(request):
    context = {}
    return render(request, 'app/checkout.html',context)


def product_woman(request):
    context = {}
    return render(request, 'app/product_woman.html',context)


def product_man(request):
    context = {}
    return render(request, 'app/product_man.html',context)


def product_kid(request):
    context = {}
    return render(request, 'app/product_kid.html',context)


def detail_product(request):
    context = {}
    return render(request, 'app/detail_product.html',context)

def bestseller(request):
    context = {}
    return render(request, 'app/bestseller.html',context)

def accessories(request):
    context = {}
    return render(request, 'app/accessories.html',context)

def aboutUs(request):
    context = {}
    return render(request, 'app/aboutUs.html',context)