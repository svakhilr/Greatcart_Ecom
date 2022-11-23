from django.urls import path
from .import views
urlpatterns = [
    path('', views.order,name='order'),
    path('payment/', views.payment, name='paymenet-page'),
    
    path('ordercomplete/', views.order_complete, name='order-complete'),
    path('cod/<int:id>/', views.cod,name='cod'),
]
