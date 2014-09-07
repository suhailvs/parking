from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
import time,json,datetime
from dateutil import parser
from homepage.models import Parking, Order
#from payments.models import Order
from django.contrib.auth.decorators import login_required
# Create your views here.

# parking details for findparking
def ajax_parkingdetails(request):
    p=Parking.objects.get(pk=request.GET['pk'])
    tformat="%I:%M:%S %p"
    week_avail=json.dumps(p.weekAvailability())
    d=dict(address=p.streetaddress,spaces=p.totalspaces,avail=week_avail if week_avail else 'false',
        desc=p.description)
        #ftime=p.fromtime.strftime(tformat),totime=p.totime.strftime(tformat))
    if p.pic: d['pic']=p.pic.url[:-4]
    return HttpResponse(json.dumps(d), mimetype="application/json")

def ajax_login(request):
    time.sleep(2)   #slowit 
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
    	auth.login(request, user)
    	return HttpResponse("1")
    return HttpResponse("Username or Password doesn't exist.")


#another function used by `ajax_savebooking`
def checkBooking(park,parktime,dur):
    if dur < 1 :return ("Please Enter a Valid Duration.",False)
    # [12, 13, 12, 12] - hours already booked on the date
    booked_hours = park.hoursBookedOnDate(parktime.date())

    # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
    avail_hours=[]    
    for hr in range(park.fromtime,park.totime+1):            
        vacants=park.totalspaces - booked_hours.count(hr)
        if vacants > 0:avail_hours.append(hr)

    wanted_hours=range(parktime.hour, parktime.hour+dur)
    print avail_hours,'<-Available | Wanted->',wanted_hours
    #if wanted_hours in avail_hours: 
    if set(wanted_hours).issubset(set(avail_hours)):
        return ('Success',True)
    return ("Please Enter a Valid Duration.",False)

# this is a Email Sending function for `ajax_savebooking`
def send_bookingConfirmation(order):
    from django.core.mail import send_mail
    from django import template
    
    str_html=template.Template("""
You're ({{order.user}}) receiving this email because you
have Successfully ordered a parking area in {{order.parking.streetaddress}}.

Order Date: {{order.order_date}}
Parking Address: {{order.parking.streetaddress}}
Parking Date:    {{order.park_date}}
Duration in Hours:  {{order.duration}} Hours

{% if order.paid %}You have paid the parking fees{% else %}
Please Pay the parking fee with in 1 hour after Order date or else 
your Order will be automatically deleted.{% endif %}
""")
    msg=str_html.render(template.Context({'order':order}))

    send_mail('Parking.com: Order for parking Space.',msg,'noreplay@parking.com',[order.user.email],fail_silently=False)


# on find parking when user order a parking spacd
def ajax_savebooking(request):
    flag=False
    if request.user.is_active:
        dur=int(request.GET['duration'])
        p=Parking.objects.get(pk=request.GET['park'])
        ptime=parser.parse(request.GET['time'])
        msg,flag=checkBooking(p,ptime,dur)
        if flag:
            #save booking
            od=Order(user=request.user,parking=p,park_date=ptime,duration=dur)
            od.save()
            # send confirmation mail
            send_bookingConfirmation(od)
            msg,flag="Successfully saved your order:%d" %od.pk, od.pk
    else:
        msg='login'
    return HttpResponse(json.dumps({'msg':msg,'status':flag}), mimetype="application/json")



# for the user home page
def userhome(request):
    time.sleep(2)
    if not request.user.is_active: return HttpResponse('login')
    curpage=request.GET['page']
    context={}
    if curpage=='editprofile':
        context['usr']=request.user
        template_url='userprofile/ajax/profile.html'
    elif curpage=='bookings':         
        context['orders']=Order.objects.filter(user=request.user)
        template_url='userprofile/ajax/orderhistory.html'

    elif curpage=='listings':
        context['parkings']=Parking.objects.filter(user=request.user)
        template_url='userprofile/ajax/myparkings.html'
    return render(request,template_url,context)