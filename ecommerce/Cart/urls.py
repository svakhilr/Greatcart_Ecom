from django.urls import path
from .import views
urlpatterns = [
    path('', views.cart ,name='cart-page'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add-product'),
    path('delete_cartitem/<int:product_id>/<int:cart_item_id>/', views.delete_cartitem, name='delete_cartitem'),
    path('remove_cartitem/<int:product_id>/<int:cart_item_id>/', views.remove_cartitem, name='remove_cartitem'),
    path('checkout/', views.checkout , name='checkout' ),
    path('wishlist/',views.view_wishlist, name='wishlist'),
    path('addwishlist', views.add_wishlist , name='addwishlist'),
    path("apply_coupon", views.Check_coupon, name="apply_coupon"),

]
