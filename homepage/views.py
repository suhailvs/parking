from django.shortcuts import render
from django.views.generic.edit import FormView
from homepage.models import ParkingForm,Parking
from django.core.urlresolvers import reverse_lazy
# Create your views here.
def viewParking(request,parking_id):
	sample=[dict(lat=18,lng=20,streetaddress='kolakkode',country='india',state='kerala'),
		dict(lat=28,lng=22,streetaddress='passs 2',country='india',state='tamilnadu')]
		
	if parking_id=='my' and request.user.is_active:
		template='pages/viewparking.html'
		d=dict(parkings=Parking.objects.filter(user=request.user))
	elif parking_id=='all':
		template='guest/parkings.html'
		d=dict(parkings=Parking.objects.all())
	else:
		template='pages/parking_details.html'
		d=dict(park_details=Parking.objects.get(pk=parking_id))
	return render(request,template,d)


class NewParking(FormView):
	template_name = 'pages/listparking.html'
	form_class = ParkingForm
	success_url = reverse_lazy('homepage.views.viewParking', args=['my'])#parkings/my

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.		
		form.instance.user = self.request.user
		form.save()
		return super(NewParking, self).form_valid(form)