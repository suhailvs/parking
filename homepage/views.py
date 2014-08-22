from django.shortcuts import render

# Create your views here.
def viewParking(request,parking_id):
	if request.user.is_active:template='pages/viewparking.html'
	else:template='guest/parkings.html'
	return render(request,template,{'results':[
		dict(lat=18,lng=20,streetaddress='kolakkode',country='india',state='kerala'),
		dict(lat=28,lng=22,streetaddress='passs 2',country='india',state='tamilnadu')
		]})

from django.views.generic.edit import FormView
from homepage.models import ParkingForm
class NewParking(FormView):
	template_name = 'pages/listparking.html'
	form_class = ParkingForm
	success_url = '/'

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.		
		form.instance.user = self.request.user
		form.save()
		return super(NewParking, self).form_valid(form)