from django.contrib import admin
from .models import Product ,Variation,ProductGallery
import admin_thumbnails


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class Productadmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock' , 'catogory', 'modified_field', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]


class Variationadmin(admin.ModelAdmin):
    list_display= ('product','variation_catogory','variation_value','is_active','created_date')
    list_editable = ('is_active',)
    list_filter = ('product','variation_catogory','variation_value',)

admin.site.register(Product,Productadmin)
admin.site.register(Variation,Variationadmin)
admin.site.register(ProductGallery)
