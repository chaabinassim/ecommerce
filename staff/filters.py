import django_filters
from orders.models import Order,OrderStatus
from django import forms

class OrderFilterForStaff(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=OrderStatus.objects.all(), widget=forms.Select(attrs={'class': 'w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500'}))
    
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
        }
