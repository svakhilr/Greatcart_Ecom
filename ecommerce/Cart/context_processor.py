from .models import Cart,Cartitem
from .views import get_cartid
def Cartcount(request):
    item_count=0

    try:
        
        cart = Cart.objects.filter(cart_id=get_cartid(request))
        if request.user.is_authenticated:
            cartitems = Cartitem.objects.all().filter(user=request.user)
        
        
        else:    
           cartitems= Cartitem.objects.all().filter(cart=cart[:1])
        for cartitem in cartitems:
            item_count+=cartitem.quantity

    except Cart.DoesNotExist:
        cartitems=0 

    return dict(item_count=item_count)