from django.shortcuts import render
from orders.models import Order
from .filters import OrderFilterForStat

def stats_view(request):
    order_filter = OrderFilterForStat(request.GET, queryset=Order.objects.all())

    filtered_orders = order_filter.qs

    # Calculate statistics based on the filtered orders
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
