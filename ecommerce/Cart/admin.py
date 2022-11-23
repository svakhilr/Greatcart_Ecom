from django.contrib import admin
from .models import Cart,Cartitem,Coupon,ReviewCoupon

# Register your models here.

class Admincartitem(admin.ModelAdmin):
    list_display = ('product','cart')

class Admincart(admin.ModelAdmin):
    list_display = ('cart_id','date_posted',)
admin.site.register(Cart,Admincart)
admin.site.register(Cartitem,Admincartitem)
admin.site.register(Coupon)
admin.site.register(ReviewCoupon)