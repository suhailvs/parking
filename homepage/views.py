from django.shortcuts import render
from django.views.generic.edit import FormView
from homepage.models import ParkingForm,Parking,Orders
from django.core.urlresolvers import reverse_lazy
from datetime import datetime
from PIL import Image as PImage
import os
from django.conf import settings
# Create your views here.
#from os.path import join as pjoin
def resize_and_crop(fname,coords):
    """
    Resize and crop profile picture.
    coords=33,44,22,33   ---x:33,y:22,x2:3,y2:4,w:33,h:32    
    >>> x=[int(i) for i in coords.split(',')]
    """
    im = PImage.open(fname)
    #box = (50, 50, 200, 300) #x1,y1,x2,y2
    box=[int(i) for i in coords.split(',')]
    region = im.crop(box)
    region.save(fname[:-4]+'_crop.jpg',"JPEG")
    region.thumbnail((160,160), PImage.ANTIALIAS)
    region.save(fname[:-4]+'_160.jpg', "JPEG")
    region.thumbnail((48,48), PImage.ANTIALIAS)
    region.save(fname[:-4]+'_48.jpg', "JPEG")
    os.remove(fname)

def FindParking(request):
	return render(request,'guest/find.html',dict(parkings=Parking.objects.all()))

def userpage(request,nm=None):
	if not nm and request.user.is_active:nm=request.user.username
	return render(request,'guest/profile.html',{'orders':Orders.objects.filter(user=request.user),
		'parkings':Parking.objects.filter(user__username=nm)})
class ShareParking(FormView):
	template_name = 'guest/share.html'
	form_class = ParkingForm
	success_url = reverse_lazy('homepage.views.userpage')#parkings/my

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.	
		#form.instance.totalspaces = self.request.POST['totalspaces']
		form.instance.fromtime = int(self.request.POST['fromtime'][:2])
		form.instance.totime = int(self.request.POST['totime'][:2])
		form.instance.user = self.request.user		
		form.save()
		if form.instance.pic:
			imfn = os.path.join(settings.MEDIA_ROOT, form.instance.pic.name)	
			resize_and_crop(imfn,self.request.POST['cropcoords'])
		return super(ShareParking, self).form_valid(form)