from orders.models import *

def get_orders_context(request):
    session,created = Session.objects.new_or_get(request)
    my_orders = Order.objects.filter(session=session)

    return {
        'my_orders':my_orders,
    }