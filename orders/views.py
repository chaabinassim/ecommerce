from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Order,Session  
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse



def order_success(request, order_id):
    # Use get_object_or_404 to fetch the order or return a 404 page if not found
    session ,created= Session.objects.new_or_get(request)
    order = get_object_or_404(Order, session=session, id=order_id)

    context = {
        'order': order
    }

    return render(request, 'order-success.html', context)


def generate_pdf_bill(request, order_id):
    order = Order.objects.get(pk=order_id)  # Replace with your order retrieval logic

    template_path = 'bill_template.html'  # Replace with the path to your HTML template
    template = get_template(template_path)
    context = {'order': order}

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('An error occurred while generating PDF')

    return response

def cart(request):
    
    return render(request,'cart.html')



