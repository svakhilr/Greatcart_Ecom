from audioop import reverse
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse

# Create your models here.
class Catogory(models.Model):
    catagory_name =  models.CharField(max_length=50, unique=True)
    slug          =  models.SlugField(max_length=50, unique=True)
    description   =  models.TextField(max_length=200 , blank=True)
    cat_img       =  models.ImageField(upload_to='catog_img')



    def __str__(self):
        return self.catagory_name

    def get_url(self):
        return reverse('products_by_category' , args=[self.slug])

    
    class Meta:
        verbose_name='catagory'
        verbose_name_plural='catagories'
