from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from orders.forms import OrderForm
from delivery.models import *
from orders.models import *
from django.http import Http404


def products(request):

    products = Product.objects.all()
    context = {
        'products' :products,
    }
    print(products)
    return render(request,'products.html',context)





def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    session ,created= Session.objects.new_or_get(request)
    states =  Wilaya.objects.all()
    fees = Fee.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.session = session
            order.save()
            return redirect("order_success",order_id=order.id)
    else:
        form = OrderForm()
        
    context ={
        'product':product,
        'states':states,
        'fees':fees,
        'form':form,
    }
   
  
    return render(request, 'product_detail.html', context)



