from django.contrib import admin
from .models import Payment , Order , OrderProduct

# Register your models here.

class Orderinline(admin.TabularInline):
    model= OrderProduct
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')

class Orderadmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines =[Orderinline]


admin.site.register(Payment)
admin.site.register(Order , Orderadmin)
admin.site.register(OrderProduct)