from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
   
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone_number', 'state', 'city','full_adress', 'quantity']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500",'placeholder': 'الاسم'}),
            'last_name': forms.TextInput(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500",'placeholder': 'اللقب'}),
            'full_adress': forms.TextInput(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500",'placeholder': 'العنوان الكامل'}),
            'state': forms.Select(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500"}),
            'city': forms.Select(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500"}),
            'phone_number': forms.NumberInput(attrs={'class': "w-full rounded border-gray-300 border p-2 focus:outline-none focus:border-blue-500",'placeholder': 'رقم الهاتف'}),
            'quantity': forms.NumberInput(attrs={'class': "rounded w-16 text-center border border-gray-300 rounded-lg py-1 px-2"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['state'].empty_label = "الولاية"
        self.fields['city'].empty_label = "البلدية"
