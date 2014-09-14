from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from mysite import settings 
from django.core.urlresolvers import reverse
# Create your views here.
from paypal.standard.forms import PayPalPaymentsForm

from homepage.models import Order
from django.views.decorators.csrf import csrf_exempt 
from django.contrib import messages
def frm_paypal(request):
    # What you want the button to do.
    #if not 'orderpk' in request.GET: 
    credit_order=Order.objects.get(pk=request.GET['orderpk'])
    if credit_order.is_expired():
        return HttpResponse("Payment Time Expired. The maximum time for completing an order is 7 minutes")
    
    site_url=settings.PAYPAL_REDIRECT_URL
    total=credit_order.parking.fee * credit_order.duration
    #print total
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": "Flexspot Parking Fee",#"name of the item",
        "invoice": credit_order.invoiceid,#str(credit_order.id).zfill(10)"unique-invoice-id1",
        "notify_url": site_url + reverse('paypal-ipn'),
        "return_url": site_url + reverse('paypal_redirect_pages', args=['success']),
        "cancel_return": site_url + reverse('paypal_redirect_pages', args=['cancel']),

    }
    # Create the instance.
    form= PayPalPaymentsForm(initial=paypal_dict) 
    return render(request,'payments/frmpaypal.html',{"form":form,"order":credit_order})

from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser)
def remove_inactive_orders(request):    
    msg='<ul>'
    orders=Order.objects.all()
    for od in orders:        
        if od.is_expired():
            msg+='<li>{0},OrderBy:{1}, OrderOn: {2}</li>'.format(od.pk,od.user.username,od.order_date)
            od.delete()
    return HttpResponse(msg+'</ul>')

@csrf_exempt
def paypal_redirect_pages(request,page):
    url=reverse('home')
    if request.user.is_active:
        if page=='success':
            messages.success(request, 'Your payment was proccessed successfully.')
        elif page=="cancel":
            #url= reverse('findparking')
            messages.warning(request, 'Your Transaction Failed!')
    return HttpResponseRedirect(url)