from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from orders.models import Order
from .filters import OrderFilterForStaff
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
        order_filter = OrderFilterForStaff(request.GET, queryset=Order.objects.all().order_by('-created_on'))
    else :
        order_filter = OrderFilterForStaff(request.GET, queryset=Order.objects.filter(staff_member__user=request.user).order_by('-created_on'))

    filtered_orders = order_filter.qs
    

    # Apply additional filtering based on selected date range (date filterting is done manulay using start  date and end date because automatic filtering cause format  error )
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        filtered_orders = filtered_orders.filter(created_on__range=[start_date, end_date])

    paginator = Paginator(filtered_orders, 5)  # Display 30 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'order_filter': order_filter,
        'page_obj': page_obj
    }
    return render(request,'staff.html',context)





@permission_required('orders.change_order')
def OrderUpdateView(request, pk):

    order = get_object_or_404(Order, pk=pk)
    if request.user == order.staff_member.user or request.user.is_staff :

        if request.method == 'POST':
            form = UpdateOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('staff_view')
        else:
            form = UpdateOrderForm(instance=order)

        context = {
            'form': form,
            'order':order,
        }
    else :
        return redirect('staff_view')
    return render(request, 'staff-order-update.html', context)