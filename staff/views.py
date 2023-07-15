from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from orders.models import Order
from .filters import OrderFilter
from django.views.generic.edit import UpdateView
from django import forms
from django.core.paginator import Paginator

# Create your views here.


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['status']
        widgets = {

            'status': forms.Select(attrs={'class': 'h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none'}),
            # Add more fields and their CSS classes as needed
        }


@permission_required('orders.change_order')
def staff_view(request):
    if request.user.is_staff:
        order_filter = OrderFilter(request.GET, queryset=Order.objects.all().order_by('-created_on'))
    else:
        order_filter = OrderFilter(request.GET, queryset=Order.objects.filter(staff_member__user=request.user).order_by('-created_on')) 
    paginator = Paginator(order_filter.qs, 5)  # Display 30 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'order_filter': order_filter,
        'page_obj': page_obj
    }
    return render(request,'staff.html',context)




class OrderUpdateView(UpdateView):
    model = Order
    form_class = UpdateOrderForm
    template_name = "staff-order-update.html"
  
   
    
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the current object to the context
        context['order'] = self.object
        return context

    