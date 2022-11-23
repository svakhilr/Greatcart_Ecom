from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register ,name='register-page'),
    path('login/', views.login, name='user-login' ),
    path('logout/', views.logout, name='user-logout' ),
    path('dashboard/',views.dashboard , name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:id>/', views.cancel_order, name='cancel_order'),
    path('register/otp/<int:id>/',views.otp,name='otp')

]
