from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
import time,json
from datetime import datetime
from homepage.models import Parking, Order
from django.conf import settings
from homepage.choices import STATE_CHOICES
from django.contrib import messages

# for the user home page
def userhome(request):
    #time.sleep(2)
    if not request.user.is_active: return HttpResponse('login')
    curpage=request.GET['page']
    context={}
    if curpage=='editprofile':
        context['usr']=request.user
        # the text of state choice, for eg:- "AL"--> "Alabama"
        if request.user.state:
            context['state_lbl'] =dict(STATE_CHOICES)[request.user.state]
        elif request.user.licenseplate:
            context['licenseplate'] =request.user.licenseplate
        template_url='userprofile/ajax/profile.html'
    elif curpage=='bookings':         
        context['orders']=Order.objects.filter(user=request.user)
        template_url='userprofile/ajax/orderhistory.html'

    elif curpage=='listings':
        context['parkings']=Parking.objects.filter(user=request.user)
        template_url='userprofile/ajax/myparkings.html'
    return render(request,template_url,context)


def ajax_parkingavailability(request):
    p=Parking.objects.get(pk=request.GET['pk'])    
    return HttpResponse(json.dumps({'hours':p.hoursAvailableOnDate(request.GET['date'])}), mimetype="application/json")

def ajax_parkingdetails(request):
    p=Parking.objects.get(pk=request.GET['pk'])
    avail=[i.name for i in p.days.all()]
    d=dict(address=p.streetaddress,desc=p.description,avail=','.join(avail),
        ftime=p.fromtime,totime=p.totime,fees=p.fee)
        #ftime=p.fromtime.strftime(tformat),totime=p.totime.strftime(tformat))
    if p.pic: d['pic']=p.pic.url[:-4]
    return HttpResponse(json.dumps(d), mimetype="application/json")
"""
def ajax_login(request):
    time.sleep(2)   #slowit 
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse("1")
        else: return HttpResponse("This account is inactive.")

    return HttpResponse("Username or Password doesn't exist.")

"""





# AJAX SAVE BOOKING FUNCTIONS
# =====================================
def checkBooking(park,parktime,dur):
    if dur < 1 :return ("Please Enter a Valid Duration.",False)

    dt=parktime.rsplit('/',1)
    hr=int(dt[1])
    avail_hours=park.hoursAvailableOnDate(dt[0])#request.GET['date'])
    wanted_hours=range(hr, hr+dur)
    print avail_hours,'<-Available | Wanted->',wanted_hours
    #if wanted_hours in avail_hours: 
    if set(wanted_hours).issubset(set(avail_hours)):
        return ('Success',True)
    return ("Please Enter a Valid Duration.",False)

# this is a Email Sending function for `ajax_savebooking`
def send_bookingConfirmation(order):
    from django.core.mail import send_mail
    from django import template
    from django.conf import settings

    ctx = {'order':order}
    subject = template.loader.render_to_string('account/email/order_not_paid_subject.txt', ctx)
    message = template.loader.render_to_string("account/email/order_not_paid.txt", ctx)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[order.user.email],fail_silently=False)

def ajax_savebooking(request):
    flag=False
    if request.user.is_active:
        #{park: "1", time: "09/15/2014/13", duration: "1"}
        dur=int(request.GET['duration'])
        p=Parking.objects.get(pk=request.GET['park'])

        ts=[int(d) for d in request.GET['time'].split('/')]
        ptime=datetime(ts[2],ts[0],ts[1],ts[3])#datetime(2014,3,16,5)
        #ptime=parser.parse(request.GET['time'])
        msg,flag=checkBooking(p,request.GET['time'],dur)
        if flag:
            #save booking
            od=Order(user=request.user,parking=p,park_date=ptime,duration=dur)
            od.save()
            od.invoiceid=str(od.id).zfill(5)# send confirmation mail
            od.save()
            send_bookingConfirmation(od)
            msg,flag="Successfully saved your order:%d" %od.pk, od.pk
    else:
        msg='login'
    return HttpResponse(json.dumps({'msg':msg,'status':flag}), mimetype="application/json")

def editparking(request,id):
    p = get_object_or_404(Parking, pk=id,user=request.user)
    #'?next=listings' p.streetaddress + request.GET['f']
    if request.GET['f']=='del':
        msg="Deleted your Parking with streetname: {0}".format(p.streetaddress)
    elif request.GET['f']=='act':
        if p.status:
            p.status=False
            msg="Deactivated your Parking with streetname: {0}".format(p.streetaddress)
        else:
            p.status=True
            msg="Activated your Parking with streetname: {0}".format(p.streetaddress)
        p.save()
        

    messages.success(request,msg)
    return HttpResponseRedirect(reverse('home')+'?next=listings')