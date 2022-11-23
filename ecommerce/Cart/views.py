from django.shortcuts import redirect, render
from store.models import Product,Variation
from .models import Cart,Cartitem,Wishlist,Coupon,ReviewCoupon
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.views.decorators.cache import never_cache

# Create your views here.

def get_cartid(request):
    cart= request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
# function to add cart items
def add_cart(request,product_id):
    print('add product')
    product= Product.objects.get(id=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        print('user authenticated')
        product_variation = []
        if request.method == 'POST':
            print(' aunthenticatd post')
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    
                    variation= Variation.objects.get(variation_catogory=key ,variation_value__iexact= value,product=product)
                    
                    print(variation)
                    product_variation.append(variation)
                    
                except:
                    pass

        print(product_variation)
        is_cart_item_exists = Cartitem.objects.filter(product=product, user=current_user).exists()
        print(is_cart_item_exists)
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            print(cart_item)
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cartitem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Cartitem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart-page')
    # If the user is not authenticated
    else:
        print('elsepart')
        product_variation=[]
        if request.method == 'POST': 
            for item in request.POST:
                key=item
                value = request.POST[key]
                try:
                    variation= Variation.objects.get(variation_catogory=key ,variation_value__iexact= value,product=product)
                    product_variation.append(variation)
                    print('user not authenticated try')
                except:
                    pass
    
        
        try:
            cart= Cart.objects.get(cart_id= get_cartid(request))
        except Cart.DoesNotExist:
            cart= Cart.objects.create(cart_id = get_cartid(request))

        cart.save()
        
        is_cartitem_exists = Cartitem.objects.filter(cart=cart, product=product).exists()
        if is_cartitem_exists:
            cart_item = Cartitem.objects.filter(product=product,cart=cart)
            print(cart_item)
            existing_var_list=[]
            id =[]
            for item in cart_item:
                existing_variation = item.variations.all()
                
                existing_var_list.append(list(existing_variation))
                
                id.append(item.id)
                
            if product_variation in existing_var_list:
                index = existing_var_list.index(product_variation)
                item_id= id[index]
                item = Cartitem.objects.get(product= product, id =item_id)
                item.quantity+=1
                item.save()
            else:
                item = Cartitem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                        
                    item.variations.clear()
                        
                    item.variations.add(*product_variation)
                    
                item.save()
            

        else:
            

            cart_item= Cartitem.objects.create(cart=cart , product = product , quantity =1)
            for item in product_variation:
                cart_item.variations.add(item)
            cart_item.save()
        
        return redirect('cart-page')


def delete_cartitem(request, product_id,cart_item_id):
    
    product= Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart_item = cart_item= Cartitem.objects.get(product=product,user= request.user ,id=cart_item_id)

    else:
        cart = Cart.objects.get(cart_id= get_cartid(request))
        cart_item= Cartitem.objects.get(product=product,cart=cart,id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()

    else:
        cart_item.delete()    
    
    return redirect('cart-page')

def remove_cartitem(request, product_id,cart_item_id):
    
    product= Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item=Cartitem.objects.get(product=product , user= request.user, id=cart_item_id)
    
    else:
        cart = Cart.objects.get(cart_id= get_cartid(request))
        cart_item= Cartitem.objects.get(cart=cart,product=product, id=cart_item_id)

    cart_item.delete()
    return redirect('cart-page')







def cart(request):

    if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user, is_active=True)
    
    else:
        cart = Cart.objects.get(cart_id = get_cartid(request))
        cart_items= Cartitem.objects.filter(cart = cart,is_active =True)
        
    
    total=0
    quantity=0
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity

    tax= round(0.02*total,2)
    grand_total=tax+ total
    
    content={
        'cart_items':cart_items,
        'quantity': quantity,
        'total' : total,
        'tax'   : tax,
        'grand_total':grand_total,
    }


    return render(request,'Cart/cart.html', content)
@login_required(login_url='user-login')
def checkout(request, total =0, quantity =0 ,cart_items=None ):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user, is_active=True)
    
        else:
            cart = Cart.objects.get(cart_id = get_cartid(request))
            cart_items= Cartitem.objects.filter(cart = cart,is_active =True)
        
        
        total=0
        quantity=0
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity+= cart_item.quantity

        tax= round(0.02*total,2)
        grand_total=tax+ total
    except ObjectDoesNotExist:
        pass
    content={
        'cart_items':cart_items,
        'quantity': quantity,
        'total' : total,
        'tax'   : tax,
        'grand_total':grand_total,
    }


    return render(request, 'Cart/checkout.html' ,content )

def view_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context={
        'wishlist':wishlist
    }
    return render(request, 'Cart/wishlist.html',context)

# def add_wishlist(request,id):
#     url = request.META.get('HTTP_REFERER')
#     product = Product.objects.get(id=id)
#     if Wishlist.objects.filter(product=product, user=request.user).exists():
#         pass
#     else:
#         Wishlist.objects.create(product=product, user=request.user)
#     return redirect(url)

def add_wishlist(request):
    flag=0
    id= request.GET["id"]
    product=Product.objects.get(id=id)
    if Wishlist.objects.filter(product=product, user=request.user).exists():
        flag=1
    else:
        Wishlist.objects.create(product=product,user=request.user)
        flag=2

    context={
        "flag":flag
    }
    return JsonResponse(context)
@never_cache
def Check_coupon(request):
    print('dfdsf')
    
    
    if "coupon_code" in request.session:
        del request.session["coupon_code"]
        del request.session["amount_pay"]
        del request.session["discount_price"]

    flag = 0
    discount_price = 0
    amount_pay = 0
    
    coupon_code = request.POST.get("coupon_code")
    grand_total = float(request.POST.get("grand_total"))
    
    if Coupon.objects.filter(code=coupon_code, coupon_limit__gte=1).exists():
        print('gkhfhkjsfkjskdfk')
        coupon = Coupon.objects.get(code=coupon_code)
        print(coupon)
        if coupon.active == True:
            flag = 1
            if not ReviewCoupon.objects.filter(
                user=request.user, coupon=coupon
            ):
                today = date.today()
                print('coupon 2')
                if coupon.valid_from <= today and coupon.valid_to >= today:
                    discount_price = grand_total - coupon.discount

                    print(discount_price)
                    amount_pay = grand_total - discount_price
                    print(amount_pay)
                    flag = 2
                    request.session["amount_pay"] = amount_pay
                    request.session["coupon_code"] = coupon_code
                    request.session["discount_price"] = discount_price

                    print("asfghjsftsfT333333")

    context = {
        "amount_pay": amount_pay,
        "flag": flag,
        "discount_price": discount_price,
        "coupon_code": coupon_code,
    }

    return JsonResponse(context)



def redeemed_coupon(request):
    if "amount_pay" in request.session:
        coupon_code = request.session["coupon_code"]
        current_user = request.user
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.coupon_limit = coupon.coupon_limit - 1
        coupon.save()
        redeem = ReviewCoupon()
        redeem.user = current_user
        redeem.coupon = coupon
        redeem.save()

        del request.session["coupon_code"]
        del request.session["amount_pay"]
        del request.session["discount_price"]
        return True
    else:
        return False
