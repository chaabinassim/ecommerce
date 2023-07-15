from django.shortcuts import render
from orders.models import *
# Create your views here.


def order_success(request,order_id):
    session ,created= Session.objects.new_or_get(request)
    order  = Order.objects.filter(session=session,id=order_id).first()

    context ={
        'order':order
    }

    return render(request,'order-success.html',context)


def cart(request):
    
    return render(request,'cart.html')



