import email
from django.shortcuts import render, redirect,get_object_or_404
from .forms import Registrationform,UserForm,UserProfileForm,Verifyform
from .models import Account,UserProfile
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from Cart.models import Cartitem , Cart
from Cart.views import get_cartid
import requests
from Orders.models import Order,OrderProduct
from store.models import Product
from . import verify

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password= form.cleaned_data['password']
            username=email.split('@')[0]
            user= Account.objects.create_user(first_name=first_name,last_name=last_name,password=password,email=email,username=username)
            user.phone_number='+91'+phone_number
            user.save()
            
            messages.success(request,f'Your account is successfully created')
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()
            
            phone_numbertest=user.phone_number
            
            verify.send(phone_numbertest)
            return redirect(f'otp/{user.id}')

            
    
    else:
        form=Registrationform()

    
    return render(request, 'Users/register.html',{'forms':form})

def otp(request, id):
    if request.method == 'POST':
        print('kjbkb')
        user=Account.objects.get(id=id)
        form = Verifyform(request.POST)
        
        if form.is_valid():
            
            code = form.cleaned_data.get('code')
            if verify.check(user.phone_number, code):
                user.is_active = True
                user.save()
                # breakpoint()
                messages.success(request, 'Registration Successfull')
                return redirect('user-login')
    else:
        form = Verifyform()
    return render(request, 'Users/otp.html', {'form': form})    




def login(request):

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email= email , password = password)
        print(user)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id =get_cartid(request))
                is_cartitem_exists= Cartitem.objects.filter(cart=cart).exists()
                if is_cartitem_exists:
                    cart_item= Cartitem.objects.filter(cart=cart)

                    product_variation=[]
                    for item  in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation)) 

                    # get the users cart items
                    cart_item = Cartitem.objects.filter(user=user)
                    ex_var_list = []
                    id=[]

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id= id[index]
                            item = Cartitem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user = user
                            item.save()

                        else:
                            cart_item = Cartitem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

                        

                    

            except:   
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('shop-home')

            

        else:
            messages.error(request , 'Invalid credentials')
            return redirect('user-login')

            

    return render(request, 'Users/login.html')
    

@login_required(login_url= 'user-login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out ')
    return redirect('user-login')


def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    # userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        # 'userprofile': userprofile,
    }
    return render(request, 'Users/dashboard.html', context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'Users/order.html', context)


def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'Users/edit_profile.html', context)

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'Users/my_order.html', context)


def cancel_order(request, id):
    product = OrderProduct.objects.get(pk=id)
    product.status = "Cancelled"
    product.save()
    item = Product.objects.get(pk=product.product.id)
    item.stock += product.quantity
    item.save()
    return redirect("my_orders")

