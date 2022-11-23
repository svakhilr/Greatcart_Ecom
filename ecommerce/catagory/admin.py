from django.contrib import admin
from .models import Catogory
# Register your models here.

class Catogoryadmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("catagory_name",)}
    list_display = ("catagory_name","slug",)

admin.site.register(Catogory,Catogoryadmin)
