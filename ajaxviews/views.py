from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
import time,json,datetime
from homepage.models import Parking,Orders
# Create your views here.
def ajax_parkingdetails(request):
    p=Parking.objects.get(pk=request.GET['pk'])
    tformat="%I:%M:%S %p"
    d=dict(pic=p.pic.url[:-4],address=p.streetaddress,spaces=p.totalspaces,isbooked=p.is_booked(),
        ftime=p.fromtime.strftime(tformat),totime=p.totime.strftime(tformat))
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
    #parking(foreignkey),park_date(date),park_timings(comaseperated ordered_hours field)
    for f in ['time','duration']:
        if request.GET[f] == "": return HttpResponse("Please fill the fields. Time and Duration")


    p=Parking.objects.get(pk=request.GET['park'])
    od=Orders(user=request.user,parking=p,fromtime=datetime.time(int(request.GET['time'])),
            duration=int(request.GET['duration']))
    try:
        od.save()
        msg="Successfully saved your order with order id:%d" %od.pk
    except:
        msg="Error"    
    return HttpResponse(msg)