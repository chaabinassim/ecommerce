from orders.models import *
from products .models import Collection
from django.db.models import Case, When, BooleanField
from customization.models import Section

def get_custom_context(request):
    session,created = Session.objects.new_or_get(request)

    my_orders = Order.objects.filter(session=session)

    featured_collections = Collection.objects.filter(is_featured=True)[:3]


    try:
        navbar_section = Section.objects.get(name="navbar")
    except Section.DoesNotExist:
        # Handle the case where the section with the given name doesn't exist
        navbar_section = None

    try:
        footer_section = Section.objects.get(name="footer")
    except Section.DoesNotExist:
        # Handle the case where the section with the given name doesn't exist
        footer_section = None   

    max_collections = [1,2,3]
    return {
        'my_orders':my_orders,
        'featured_collections':featured_collections,
        'max_collections':max_collections,
        'navbar_section':navbar_section,
        'footer_section':footer_section,
    }