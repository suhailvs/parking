from django.shortcuts import render
from mysite import settings 
from django.core.urlresolvers import reverse
# Create your views here.
from paypal.standard.forms import PayPalPaymentsForm

from homepage.models import Order
from django.views.decorators.csrf import csrf_exempt 

def frm_paypal(request):
    # What you want the button to do.
    #if not 'orderpk' in request.GET: 
    credit_order=Order.objects.get(pk=request.GET['orderpk'])    
    site_url=settings.PAYPAL_REDIRECT_URL

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": credit_order.parking.fee,#"1.00",
        "item_name": "Flexspot Parking Fee",#"name of the item",
        "invoice": credit_order.invoiceid,#str(credit_order.id).zfill(10)"unique-invoice-id1",
        "notify_url": site_url + reverse('paypal-ipn'),
        "return_url": site_url + reverse('paypal_redirect_pages', args=['success']),
        "cancel_return": site_url + reverse('paypal_redirect_pages', args=['cancel']),

    }
    # Create the instance.
    form= PayPalPaymentsForm(initial=paypal_dict) 
    return render(request,'payments/frmpaypal.html',{"form":form})

@csrf_exempt
def paypal_redirect_pages(request,page):
    return render(request,'payments/redirect_pages.html',{'page':page})