from django.shortcuts import render

# Create your views here.
def viewParking(request,parking_id):
	if request.user.is_active:template='pages/viewparking.html'
	else:template='guest/parkings.html'
	return render(request,template)
