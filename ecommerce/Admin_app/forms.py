from django import forms
from Users.models import  Account
from store.models import Product
from django.forms.widgets import CheckboxInput, FileInput, TextInput
from django.forms import ModelForm
from catagory.models import Catogory
from Cart.models import Coupon

class  Editproduct(ModelForm):
    
    product_name = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "product_name"}),
    )
    description = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"placeholder": "description"}),
    )
    price = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "price"}),
    )
    # images = forms.ImageField(required=True,widget=FileInput)
    stock = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "stock"}),
    )
    is_available = forms.BooleanField(
        required=True, widget=CheckboxInput(attrs={"placeholder": "Status"})
    )
   
    class Meta:
        
        model = Product
        fields = ['product_name','description','price', 'stock','is_available','product_img','catogory','offer' ]

    def _init_(self, *args, **kwargs):
        super(Editproduct, self)._init_(
            *args, **kwargs
        ) 

class Productform(ModelForm):
    description = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"placeholder": "description"}),
    )
    
    class Meta:
        model= Product
        fields=['product_name','slug','description','price','stock','product_img','catogory','offer']

class Addcatogory(ModelForm):

    description = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"placeholder": "description"}),
    )

    class Meta:
        model = Catogory
        fields=['catagory_name','slug','description','cat_img']

class Addcoupon(ModelForm):

    

    class Meta:
        model=Coupon
        fields=['coupon_name','code','coupon_limit','valid_from','valid_to','discount']