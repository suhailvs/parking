from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

# Create your views here.
def viewParking(request,parking_id):
	if request.user.is_active:template='pages/viewparking.html'
	else:template='guest/parkings.html'
	return render(request,template)


def ajax_login(request):
    #time.sleep(2)   #slowit 
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
    	auth.login(request, user)
    	return HttpResponse("1")
    return HttpResponse("Username or Password doesn't exist.")