from django.shortcuts import render,redirect
from Cart.models import Cartitem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct,Sales
import datetime
import json
from store.models import Product
from django.http import JsonResponse
from Cart.views import redeemed_coupon
from django.urls import reverse
# Create your views here.

def payment(request):
    body = json.loads(request.body)
    order= Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(body)
    payment = Payment(
        user = request.user,
        payment_id= body['transID'],
        amount_paid = order.order_total,
        status = body['status'],
        payment_method= body['payment_method']
    )

    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cartitems = Cartitem.objects.filter(user=request.user)

    for item in cartitems:
        orderproduct = OrderProduct()
        orderproduct.order_id= order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price*item.quantity
        orderproduct.ordered = True
        orderproduct.save()

        cartitem = Cartitem.objects.get(id=item.id)
        product_variation = cartitem.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        product= Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
     
        


    Cartitem.objects.filter(user=request.user).delete()

     # for review coupons and reduce count
    check_coupon = redeemed_coupon(request)
    print(check_coupon)

    data ={
        "order_id": order.order_number,
        "payment_id": payment.payment_id,
    }  

    return JsonResponse(data)

def cod(request,id):
    order=Order.objects.get(id=id,user=request.user)
    payment = Payment(
        user = request.user,
        payment_id= order.order_number,
        amount_paid = order.order_total,
        status = 'COMPLETED',
        payment_method= 'COD'
    )
    
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cartitems = Cartitem.objects.filter(user=request.user)

    for item in cartitems:
        orderproduct = OrderProduct()
        orderproduct.order_id= order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price*item.quantity
        orderproduct.ordered = True
        orderproduct.save()

        cartitem = Cartitem.objects.get(id=item.id)
        product_variation = cartitem.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        product= Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
     
        


    Cartitem.objects.filter(user=request.user).delete()

     # for review coupons and reduce count
    check_coupon = redeemed_coupon(request)
    print(check_coupon)

    param = (
        "order_number="
        + order.order_number
        + "&payment_id="
        + payment.payment_id
    )

    redirect_url = reverse("order-complete")
    return redirect(f"{redirect_url}?{param}")



def order(request, total=0 , quantity=0,grand_total=0,tax=0):
    current_user = request.user
    cart_items= Cartitem.objects.filter(user=current_user)
    cart_items_count= cart_items.count()
    if cart_items_count <= 0:
        return redirect('store-page')

    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity

    tax=round(0.02*total,2)
    
    grand_total = total+ tax

    if "discount_price" in request.session:
        grand_total = request.session["discount_price"]
    

    
    if request.method == 'POST':
        form= OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.user = current_user
            data.order_total = grand_total
            data.tax= tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, order_number=order_number,is_ordered=False)
            
            content={
                'order':order,
                'total':total,
                'tax': tax,
                'grand_total': grand_total,
                'cart_items':cart_items
            }
            return render(request,'Orders/payment.html' , content)
    else:
        return redirect('checkout')
        
    


def order_complete(request):
    order_number= request.GET.get('order_number')
    trans_id = request.GET.get('payment_id')

    try:
        order= Order.objects.get(order_number=order_number)
        order_product= OrderProduct.objects.filter(order_id=order.id)
        
        subtotal = 0
        for i in order_product:
            subtotal += i.product_price 

        tax_added=order.tax+subtotal


        context={'order_number':order_number,
                  'order_product':order_product,
                  'trans_id': trans_id,
                  'order': order,
                  'order_products': order_product,
                  'sub_total':subtotal,
                  'tax_added':tax_added}

        return render(request, 'Orders/ordercomplete.html',context)
    except(Order.DoesNotExist,Payment.DoesNotExist):
        return redirect('store-page')
    