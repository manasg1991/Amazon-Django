from django.shortcuts import render
from django.views import View
from Store.models import Product 
# Create your views here.
def home(request):
    product =Product.objects.all().filter(is_available=True)
    context ={
        'product':product 
    }
    return render(request,'amazon/home.html',context)
    
