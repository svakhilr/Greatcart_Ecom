from .models import Catogory

def menu_links(request):
    link = Catogory.objects.all()
    return dict(link=link)