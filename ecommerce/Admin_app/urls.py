from django.urls import path
from .import views
urlpatterns = [
    path('home/', views.admin_home,name='admin-home'),
    path('products/',views.product_list , name='product-list'),
    path('', views.signin, name='admin-signin' ),
    path('block/<int:id>/', views.userblock ,name='block' ),
    path('unblock/<int:id>/', views.user_unblock ,name='unblock' ),
    path('signout/', views.signout, name='admin-signout'),
    path('editproduct/<int:id>/', views.edit_product, name= 'editproduct'),
    path('dashboard/', views.admin_dashboard, name='admin-dash'),
    path('addproduct/', views.add_product , name='add-product'),
    path('catogory/', views.catogory_list, name='catogory-list'),
    path('<int:id>/', views.delete_catogory, name= 'delete-catogory'),
    path('addcatogory/',views.add_catogery, name='add-catogory'),
    path('orderlist/', views.order_list, name='orderproduct-list'),
    path('change/<int:id>/', views.change_status, name= 'change_status'),
    path('coupons/', views.couponview, name='viewcoupons'),
    path('addcoupon/', views.add_coupon, name='add-coupon'),
    path('deletecoupon/<int:id>', views.delete_coupon, name='delete-coupon'),
    path('admindash/', views.dash, name='admindash')
    ]
