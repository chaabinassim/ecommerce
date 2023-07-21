import django_filters
from orders.models import Order,StaffMember
from django import forms

class OrderFilter(django_filters.FilterSet):
    staff_member = django_filters.ModelChoiceFilter(queryset=StaffMember.objects.all(), widget=forms.Select(attrs={'class': 'w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500'}))
    
    class Meta:
        model = Order
        fields = {
            'staff_member': ['exact'],
        }
