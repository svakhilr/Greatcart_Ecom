from email.policy import default
from enum import unique
from random import choices
from django.db import models
from catagory.models import Catogory
from django.urls import reverse
from Offer.models import Offers

# Create your models here.

class Product(models.Model):
    product_name  =  models.CharField(max_length=200, unique=True)
    slug          =  models.SlugField(max_length=200, unique=True)
    description   =  models.CharField(max_length=500,blank=True)
    price         =  models.IntegerField()
    stock         =  models.IntegerField()
    is_available  =  models.BooleanField(default=True)
    product_img   =  models.ImageField(upload_to= 'product_img')
    catogory      =  models.ForeignKey(Catogory , on_delete=models.CASCADE)
    created_field =  models.DateTimeField(auto_now_add=True)
    modified_field=  models.DateTimeField(auto_now=True)
    offer         =  models.ForeignKey(Offers, blank=True,null=True,on_delete=models.SET_NULL)
    actual_price  =  models.IntegerField(null=True , blank=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.catogory.slug,self.slug])

    




class VariationManager(models.Manager):
    # def colors(self):
    #     return super(VariationManager,self).filter(variation_catogory='color', is_active=True)

    def size(self):
        return super(VariationManager,self).filter(variation_catogory='size', is_active=True)


variation_category_choice=( 
                             ('size','size'),)

            

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_catogory = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active= models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    objects =VariationManager()

    def __str__(self):
        return self.variation_value



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'