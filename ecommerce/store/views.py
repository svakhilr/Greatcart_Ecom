from ast import keyword
from itertools import product
from tkinter import E
from django.http import HttpResponse
from django.shortcuts import redirect, render , get_object_or_404
from .models import Product,ProductGallery
from catagory.models import Catogory
from Cart.models import Cartitem,Cart
from Cart.views import get_cartid
from django.db.models import Q

# Create your views here.

def store(request,category_slug=None):
    categories = None
    product  = None
    if category_slug != None:
        categories = get_object_or_404(Catogory , slug = category_slug)
        product    = Product.objects.filter(catogory= categories , is_available= True)
        product_count = product.count()

    else:
        product = Product.objects.all().filter(is_available=True)
        product_count= product.count()
    content ={
        "products":product,
        "products_count":product_count
        }
    return render(request , 'store/store.html', content)

def product_detail(request,category_slug,product_slug):

    try:
        single_product=Product.objects.get(catogory__slug=category_slug, slug=product_slug)
        iscart_id= Cartitem.objects.filter(product=single_product,cart__cart_id=get_cartid(request)).exists()
        
        

    except Exception as e:
        raise e

    # product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {"single_product":single_product,
               "iscart_id" : iscart_id,
               "product_gallery":product_gallery    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(product_name__icontains=keyword)| Q(description__icontains= keyword))
            product_count= products.count()

            context={ 
                'products':products,
                "products_count":product_count
                }

    return render(request, 'store/store.html',context)