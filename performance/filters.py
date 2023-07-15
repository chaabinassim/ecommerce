import django_filters
from orders.models import Order

class OrderFilterForStat(django_filters.FilterSet):
    created_on = django_filters.DateRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-input w-full px-3 py-2 rounded-md placeholder-gray-400 focus:outline-none focus:ring focus:border-blue-500 bg-gray-100 datetimepicker'}),
        field_name='created_on',
        label='Created on'
    )
    class Meta:
        model = Order
        fields = {
            'staff_member': ['exact'],
            'created_on': ['date__gte', 'date__lte'],
        }
