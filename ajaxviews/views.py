from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
import time,json,datetime
from dateutil import parser
from homepage.models import Parking,Orders
# Create your views here.
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

def checkBooking(park,parktime,dur):
    if dur < 1 :return ("Please Enter a Valid Duration.",False)
    # [12, 13, 12, 12] - hours already booked on the date
    booked_hours = park.hoursBookedOnDate(parktime.date())

    # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]    
    for hr in range(park.fromtime.hour,park.totime.hour+1):            
        if parktime.hour <= hr <= parktime.hour+dur:
            vacants=park.totalspaces - booked_hours.count(hr)
            if vacants < 1:
                return ("Sorry Maximum Duration is {0}.".format(parktime.hour-hr),False)

    return ('Success',True)

def ajax_savebooking(request):
    flag=False
    if request.user.is_active:
        dur=int(request.GET['duration'])
        p=Parking.objects.get(pk=request.GET['park'])
        ptime=parser.parse(request.GET['time'])
        msg,flag=checkBooking(p,ptime,dur)
        if flag:
            #save booking
            od=Orders(user=request.user,parking=p,park_date=ptime,duration=dur)
            od.save()
            msg,flag="Successfully saved your order:%d" %od.pk, od.pk
    else:
        msg='login'
    return HttpResponse(json.dumps({'msg':msg,'status':flag}), mimetype="application/json")
     
"""
def checkBookings(park,parktime,dur):
    if dur < 1 :return ("Please Enter a Valid Duration.",False)

    #check for availablity for give time
    # [12, 13, 12, 12] - hours already booked on the date
    booked_hours = park.hoursBookedOnDate(parktime.date())
    print '%s - hours already booked on the date ' % booked_hours

    # [13, 14, 15, 16, 17, 18, 19, 20, 21, 22] - hours need to book for the date
    print '%s - hours need to book for the date' % range(ptime.hour,ptime.hour+dur)

    # Maximum duration available continously from given datetime         
    # check ptime.hour available, then check ptime.hour + 1 available.... break if not available
    #=======================================================================     
    # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
    avail_hours=[]
    for hr in range(p.fromtime.hour,p.totime.hour+1):            
        if ptime.hour <= hr <= ptime.hour+dur:
            vacants=p.totalspaces - booked_hours.count(hr)
            if vacants < 1: 
                break

            avail_hours.append(hr)
            
        else:
            # if not hours selected by driver
            print 'hours not needed for the driver'
    print '%s - hours duration available continously' % avail_hours
    #--------------
"""