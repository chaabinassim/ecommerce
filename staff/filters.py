import django_filters
from orders.models import Order,OrderStatus
from django import forms

class OrderFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=OrderStatus.objects.all(), widget=forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-md placeholder-gray-400 focus:outline-none focus:ring focus:border-blue-500 bg-gray-100'}))
    created_on = django_filters.DateRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-input w-full px-3 py-2 rounded-md placeholder-gray-400 focus:outline-none focus:ring focus:border-blue-500 bg-gray-100 datetimepicker'}),
        field_name='created_on',
        label='Created on'
    )
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_on': ['date__gte', 'date__lte'],
        }
