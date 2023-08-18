from django.shortcuts import render
from orders.models import Order
from .filters import OrderFilter
from django.contrib.auth.decorators import permission_required

@permission_required('orders.change_order')
def stats_view(request):
    order_filter = OrderFilter(request.GET, queryset=Order.objects.all())
    filtered_orders = order_filter.qs

    # Apply additional filtering based on selected staff member
    staff_member = request.GET.get('staff_member')
    if staff_member:
        filtered_orders = filtered_orders.filter(staff_member=staff_member)

    # Apply additional filtering based on selected date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        filtered_orders = filtered_orders.filter(created_on__range=[start_date, end_date])

    total_orders = filtered_orders.count()
    confirmed_orders = filtered_orders.filter(status__name='Confirmed').count()
    canceled_orders = filtered_orders.filter(status__name='Canceled').count()

    stats = {
        'total_orders': total_orders,
        'confirmed_orders': confirmed_orders,
        'canceled_orders': canceled_orders,
        'total_orders_percentage': 100.0,
        'confirmed_orders_percentage': (confirmed_orders * 100.0 / total_orders) if total_orders > 0 else 0,
        'canceled_orders_percentage': (canceled_orders * 100.0 / total_orders) if total_orders > 0 else 0
    }

    context = {
        'order_filter': order_filter,
        'stats': stats,
        'filtered_orders': filtered_orders,
    }

    return render(request, 'stats.html', context)