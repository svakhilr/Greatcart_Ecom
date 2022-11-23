from django.contrib import admin
from .models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.

class Accountadmin(UserAdmin):
    list_display = ('email','first_name' ,'last_name', 'date_joined', 'is_admin', 'is_staff','is_block' )

    filter_horizontal= ()
    list_filter= ()
    fieldsets=()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account,Accountadmin)
admin.site.register(UserProfile,UserProfileAdmin)
