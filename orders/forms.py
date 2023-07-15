from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
   
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone_number', 'state', 'city','full_adress', 'quantity']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none",'placeholder': 'الاسم'}),
            'last_name': forms.TextInput(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none",'placeholder': 'اللقب'}),
            'full_adress': forms.TextInput(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none",'placeholder': 'العنوان الكامل'}),
            'state': forms.Select(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none"}),
            'city': forms.Select(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none"}),
            'phone_number': forms.NumberInput(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none",'placeholder': 'رقم الهاتف'}),
            'quantity': forms.NumberInput(attrs={'class': "h-10 px-4 py-2 w-full text-sm text-gray-400 border border-blueGray-800 bg-transparent outline-none"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['state'].empty_label = "الولاية"
        self.fields['city'].empty_label = "البلدية"
