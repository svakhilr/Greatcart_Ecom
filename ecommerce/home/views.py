from django.shortcuts import render
from store.models import Product

# Create your views here.

def home(request): 
    product = Product.objects.filter(is_available=True)
    content ={ "products":product }
    return render(request,"home/home.html", content)