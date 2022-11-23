from email.policy import default
from django.db import models
from store.models import Product,Variation
from Users.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length = 210,blank=True) 
    date_posted = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.cart_id

class Cartitem(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation , blank=True)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  self.product

    def subtotal(self):
        return self.quantity * self.product.price


class Wishlist(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=25)
    code = models.CharField(max_length=25, unique=True)
    coupon_limit = models.IntegerField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class ReviewCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return self.coupon.coupon_name

