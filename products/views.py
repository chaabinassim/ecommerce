from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from orders.forms import OrderForm
from delivery.models import *
from orders.models import *
from django.http import Http404

def product_list(request):
    collections = Collection.objects.all()
    products= Product.objects.all()
    return render(request, 'product_list.html', {'collections': collections, 'products': products})


def product_detail(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)
    session ,created= Session.objects.new_or_get(request)
    states = Wilaya.objects.all()
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
        'form':form,
        'fees':fees
    }
  
    return render(request, 'product_detail.html', context)



