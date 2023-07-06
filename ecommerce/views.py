from django.shortcuts import render,redirect
from products.models import *

def home(request):
    collections = Collection.objects.all()
    featured_products  = Product.objects.all()
    context ={
        'collecions':collections,
        'featured_products'  :featured_products
    }
    return render(request,'home.html',context)