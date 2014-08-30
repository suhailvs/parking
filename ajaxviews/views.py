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

def ajax_savebooking(request):       
    p=Parking.objects.get(pk=request.GET['park'])
    msg="Not available for selected time." 
    flag=False

    #check for availablity for give time
    dur=int(request.GET['duration'])
    ptime=parser.parse(request.GET['time'])
    o_time=int(time.mktime(ptime.timetuple()))
    week_avail=p.weekAvailability()
    if str(o_time) in week_avail:
        if week_avail[str(o_time)] >= dur:
            od=Orders(user=request.user,parking=p,park_date=ptime,duration=dur)
            od.save()
            msg="Successfully saved your order:%d" %od.pk
            flag=od.pk
        else:
            msg="only %d hours available" %week_avail[o_time]

    return HttpResponse(json.dumps({'msg':msg,'status':flag}), mimetype="application/json")
        