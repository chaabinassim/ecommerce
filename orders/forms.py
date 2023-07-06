from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
   
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone_number', 'state', 'city','full_adress', 'quantity']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",'placeholder': 'الاسم'}),
            'last_name': forms.TextInput(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",'placeholder': 'اللقب'}),
            'full_adress': forms.TextInput(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",'placeholder': 'العنوان الكامل'}),
            'state': forms.Select(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"}),
            'city': forms.Select(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"}),
            'phone_number': forms.NumberInput(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500",'placeholder': 'رقم الهاتف'}),
            'quantity': forms.NumberInput(attrs={'class': "block w-full p-4  rounded-lg  sm:text-md  bg-gray-600 border border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['state'].empty_label = "الولاية"
        self.fields['city'].empty_label = "البلدية"
