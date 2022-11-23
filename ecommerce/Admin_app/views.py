from django.shortcuts import render,redirect
from Users.models import Account
from store.models import Product
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import Editproduct,Productform,Addcatogory,Addcoupon
from catagory.models import Catogory
from Orders.models import OrderProduct
from Cart.models import Coupon
from Orders.models import Payment
# Create your views here.
# @login_required(login_url="admin-signin")

def admin_dashboard(request):
    return render(request, "Admin_app/dashboard.html")

@login_required(login_url="admin-signin")
def admin_home(request):
    users = Account.objects.filter(is_admin = False)
    print(users)
    context = {
        'users':users
    }
    return render(request,"Admin_app/userdashboard.html", context)

@login_required(login_url="admin-signin")
def product_list(request):
    products= Product.objects.all()
    context={
        'products':products
    }

    return render(request, 'Admin_app/product.html', context )

def signin(request):

    if request.method == "POST":
        email = request.POST["email"]
        password= request.POST["password"]
        user = auth.authenticate(
            email=email, password=password
        )

        if user is not None and user.is_admin:
            auth.login(request, user)
            return redirect("admin-home")
        
        else:
            messages.error(request, "You are not an admin")
            return redirect("admin-signin")

    return render(request, "Admin_app/adminsignin.html")


@login_required(login_url="admin-signin")
def signout(request):
    auth.logout(request)
    return redirect('admin-signin')


def userblock(request, id):
    
    user= Account.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect("admin-home")

def user_unblock(request,id):
    user = Account.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect("admin-home")

def edit_product(request,id):
    product=Product.objects.get(id=id)
    form= Editproduct(instance= product)
    if request.method == "POST":
        form= Editproduct(request.POST, request.FILES , instance= product)
        if form.is_valid():
            product=form.save()
            if product.offer is not None:
                product.actual_price = product.price
                product.price = int(product.actual_price-(product.actual_price*product.offer.discout/100))
                print(product.price,'price')
                print(product.actual_price,'actual_price')
                product.save()
            return redirect('product-list')
    
    context= {'form':form}
    return render(request, 'Admin_app/editproduct.html',context)

def add_product(request):
    form=Productform()
    if request.method == "POST":
        form= Productform(request.POST, request.FILES)
        if form.is_valid():
            product=form.save()
            print('vnbbvb')
            if product.offer is not None:
                product.actual_price = product.price
                product.price = int(product.actual_price-(product.actual_price*product.offer.discout/100))
                print(product.price,'price')
                print(product.actual_price,'actual_price')
                product.save()

            return redirect('product-list')

    context={"form":form}
    return render(request, 'Admin_app/addproduct.html', context)

def  catogory_list(request):
    catogories = Catogory.objects.all()
    context={'catogories':catogories}
    return render(request,"Admin_app/catogery.html",context)

def delete_catogory(request,id):
    catogory= Catogory.objects.get(id=id)
    catogory.delete()
    return redirect('catogory-list') 

def add_catogery(request):
    form=Addcatogory()
    if request.method == 'POST':
        form= Addcatogory(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catogory-list')

    context={"form":form}
    return render(request, 'Admin_app/addcatogery.html' , context)


def order_list(request):
    order_products= OrderProduct.objects.all()
    context={'order_products':order_products}
    return render(request, 'Admin_app/orderproductlist.html',context)

def change_status(request,id):
    if request.method == 'POST':
        status=request.POST['status']
        product= OrderProduct.objects.get(id=id)
        product.status=status
        product.save()
        return redirect('orderproduct-list')


def couponview(request):
    coupons=Coupon.objects.all()
    context={'coupons':coupons}
    return render(request, 'Admin_app/coupon.html',context)


def add_coupon(request):
    
    if request.method == 'POST':
        form= Addcoupon(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewcoupons')

    else:
        form= Addcoupon()

    context = {'form':form}

    return render(request,'Admin_app/addcoupon.html',context)

def delete_coupon(request,id):
    coupon=Coupon.objects.get(id=id)
    coupon.delete()
    return redirect('viewcoupons')

def dash(request):
    New=0
    Accepted=0
    Completed=0
    Cancelled=0
    products=Product.objects.all().count()
    users=Account.objects.all().count()
    sales=OrderProduct.objects.all().count()
    revenue= Payment.objects.all()
    amount=0
    for i in revenue:
        amount+=float(i.amount_paid)
    amt=round(amount,2)
    labels=[]
    data=[]

    queryset= OrderProduct.objects.all().order_by('-created_at')
    for product in queryset:
        if product.status == 'New':
            New+=1
        elif product.status == 'Accepted':
            Accepted+=1
        elif product.status == 'Completed':
            Completed+=1
        else:
            Cancelled+=1

    print(New)
    print(Accepted)
    print(Completed)
    print(Cancelled)

    labels=["New","Accepted","Completed","Cancelled"]
    data=[New,Accepted,Completed,Cancelled]
         
    
    context={
        'product_count':products,
        'user_count' : users,
        'sales_count' : sales,
        'revenue' : amt,
        'data':data,
        'labels':labels
    }
    return render(request,'Admin_app/admindash.html',context)
    








    

    
    