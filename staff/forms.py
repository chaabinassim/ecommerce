from django import forms
from orders.models import Order

class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['status','center','is_stopdesk','state']
        widgets = {

            'status': forms.Select(attrs={'class': 'w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-yellow-500'}),
            'center': forms.Select(attrs={'class': 'w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-yellow-500'}),
            'state': forms.Select(attrs={'class': 'w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-yellow-500'}),
            # Add more fields and their CSS classes as needed
        }