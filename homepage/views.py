from django.shortcuts import render
from django.views.generic.edit import FormView
from homepage.models import ParkingForm,Parking
from django.core.urlresolvers import reverse_lazy
from datetime import datetime
# Create your views here.

def FindParking(request):
	return render(request,'guest/find.html',dict(parkings=Parking.objects.all()))

def userpage(request,nm):
	return render(request,'guest/profile.html',{'parkings':Parking.objects.filter(user__username=nm)})
class ShareParking(FormView):
	template_name = 'guest/share.html'
	form_class = ParkingForm
	success_url = reverse_lazy('homepage.views.viewParking', args=['my'])#parkings/my

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.	
		form.instance.totalspaces = self.request.POST['totalspaces']
		form.instance.fromtime = datetime.strptime(self.request.POST['fromtime'],'%I:%M %p')#11:30 PM
		form.instance.totime = datetime.strptime(self.request.POST['totime'],'%I:%M %p')
		form.instance.user = self.request.user
		form.save()
		return super(ShareParking, self).form_valid(form)