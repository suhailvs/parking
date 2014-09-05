from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic.edit import FormView
from homepage.models import Parking,Orders
from homepage.forms import ParkingForm
import time
from PIL import Image as PImage
import os
from django.conf import settings
from django.contrib import messages

from django.views.generic.base import View
class MyHome(View):
	def get(self, request):
		if not request.user.is_active:
			return render(request,'home.html')		
		sidemenu={'editprofile':'Profile','bookings':'My Bookings',
		'listings':'My Parking Areas','credits':'My Credits'}
		return render(request,'userprofile/home.html',{'sidemenu':sidemenu})
	def post(self,request):
		if not request.user.is_active:
			return render(request,'home.html')
		if request.POST['submit']=='profileupdate':
			for key,value in request.POST.iteritems():
				if key in ['last_name','first_name','email']:
					setattr(request.user,key,value)	
			request.user.save()		
			messages.success(request, 'Profile updated successfully.')		
			return HttpResponseRedirect(reverse('home'))

"""
# why did these need????
def FindParking(request):
	return render(request,'guest/find.html',dict(parkings=Parking.objects.all()))

def userpages(request,nm=None):
	if not nm and request.user.is_active:nm=request.user.username
	return render(request,'guest/profile.html',{'orders':Orders.objects.filter(user=request.user),
		'parkings':Parking.objects.filter(user__username=nm)})
"""


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
    #region.thumbnail((48,48), PImage.ANTIALIAS)
    #region.save(fname[:-4]+'_48.jpg', "JPEG")
    os.remove(fname)

class ShareParking(FormView):
	template_name = 'userprofile/share.html'
	form_class = ParkingForm
	success_url = '/'#reverse_lazy('homepage.views.userpage')#parkings/my

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.	
		#form.instance.totalspaces = self.request.POST['totalspaces']
		ftime=time.strptime(self.request.POST['fromtime'],'%I:%M %p')
		ttime=time.strptime(self.request.POST['totime'],'%I:%M %p')		
		form.instance.fromtime = ftime.tm_hour
		form.instance.totime = ttime.tm_hour
		form.instance.user = self.request.user		
		form.save()
		if form.instance.pic:
			imfn = os.path.join(settings.MEDIA_ROOT, form.instance.pic.name)	
			resize_and_crop(imfn,self.request.POST['cropcoords'])
		return super(ShareParking, self).form_valid(form)


from account.views import SignupView
from homepage.forms import CustSignupForm

class CustSignupView(SignupView):
	form_class = CustSignupForm
	def after_signup(self, form):
		self.update_profile(form)
		super(CustSignupView, self).after_signup(form)

	def update_profile(self, form):
		profile = self.created_user
		profile.state = form.cleaned_data["state"]
		if form.cleaned_data["is_owner"]=='0':
			profile.licenseplate = form.cleaned_data["licenseplate"]
		profile.save()
