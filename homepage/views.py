from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic.edit import FormView
from homepage.models import Parking,Order
#from payments import Orders
from homepage.forms import ParkingForm,ParkingSubForm
import time,os,datetime
from PIL import Image as PImage
from django.conf import settings
from django.contrib import messages

from django.views.generic.base import View
class MyHome(View):
	def get(self, request):
		if not request.user.is_active:
			return render(request,'home.html')
		elif request.user.is_superuser:
			return render(request,'admin_home.html')
		sidemenu={'editprofile':'Profile','bookings':'My Bookings',
		'listings':'My Parking Areas'}
		return render(request,'userprofile/home.html',{'sidemenu':sidemenu,'next':request.GET.get('next','editprofile')})
	def post(self,request):
		if not request.user.is_active:
			return render(request,'home.html')
		if request.POST['submit']=='profileupdate':
			for key,value in request.POST.iteritems():
				if key in ['last_name','first_name']:
					setattr(request.user,key,value)	
			request.user.save()		
			messages.success(request, 'Profile updated successfully.')		
			return HttpResponseRedirect(reverse('home'))


class FindParkings(View):
	def get(self, request):
		return render(request,'userprofile/find_w1.html',{'parkings':Parking.objects.filter(status=True)})
	def post(self,request):
		if 'park_pk' in request.POST:
			if not request.user.is_active:return HttpResponseRedirect(reverse('account_login')+"?next="+reverse('findparking'))
			p=Parking.objects.get(pk=request.POST['park_pk'])
			if request.user==p.user:
				return render(request,'errorpages/error_404.html',{'error_msg':'Why are you Booking your own Parking Area?'})
			elif request.user.licenseplate=='':
				return render(request,'errorpages/error_404.html',{'error_msg':'You seems login as Parking Owner. To book parking, please <a href="#">add</a> your state and a licenseplate number first.'})
			return render(request,'userprofile/find_w2.html',{'avail':p.AvailableDays(),'parking':p,'servertime':datetime.datetime.today()})

	
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
    try:
        region.save(fname[:-4]+'_crop.jpg',"JPEG")
    except IOError:
        region.convert('RGB').save(fname[:-4]+'_crop.jpg',"JPEG")
    region.thumbnail((160,160), PImage.ANTIALIAS)
    try:region.save(fname[:-4]+'_160.jpg', "JPEG")
    except IOError:region.convert('RGB').save(fname[:-4]+'_160.jpg', "JPEG")
    #region.thumbnail((48,48), PImage.ANTIALIAS)
    #region.save(fname[:-4]+'_48.jpg', "JPEG")
    os.remove(fname)

class ShareParkingStuff(View):
	def get(self, request,id=None):
		if id:
			p = get_object_or_404(Parking, pk=id)
			if p.user != request.user:return HttpResponse('Forbidden')
			d=dict(first_form=ParkingForm(instance=p),edit=id,
				second_form=ParkingSubForm({'fromtime': p.fromtime, 'totime': p.totime,'fee':p.fee,'totalspaces':p.totalspaces}))
		else:
			d=dict(first_form=ParkingForm(),second_form=ParkingSubForm())
		return render(request,'userprofile/share.html',d)

	def post(self,request,id=None):
		if id:#'id' in request.POST:
			p = get_object_or_404(Parking, pk=id)#request.POST['id'])
			if p.user != request.user:return HttpResponse('Forbidden')
		else:p = Parking(user=request.user)

		form1=ParkingForm(request.POST,request.FILES,instance=p)
		form2=ParkingSubForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			form1.instance.fromtime = form2.cleaned_data['fromtime']
			form1.instance.totime=form2.cleaned_data['totime']
			form1.instance.totalspaces = form2.cleaned_data['totalspaces']
			form1.instance.fee=form2.cleaned_data['fee']
			form1.save()
			if form1.instance.pic:
				imfn = os.path.join(settings.MEDIA_ROOT, form1.instance.pic.name)
				resize_and_crop(imfn,request.POST['cropcoords'])
			
			return HttpResponseRedirect(reverse('home'))
		d=dict(first_form=form1,second_form=form2)
		return render(request,'userprofile/share.html',d)


from account.views import SignupView,LoginView
from homepage.forms import CustSignupForm

class CustSignupView(SignupView):
	form_class = CustSignupForm
	def after_signup(self, form):
		self.update_profile(form)
		super(CustSignupView, self).after_signup(form)

	def update_profile(self, form):
		profile = self.created_user
		profile.username=str(profile.id)
		profile.state = form.cleaned_data["state"]
		if form.cleaned_data["is_owner"]=='0':
			profile.licenseplate = form.cleaned_data["licenseplate"]
		profile.save()
		print ('send Welcome')

	def generate_username(self, form):
		# do something to generate a unique username (required by the
		# Django User model, unfortunately)		
		return '0.0'

from account.forms import LoginEmailForm
class CustLoginView(LoginView):
    form_class = LoginEmailForm


def parking_info(request,pk):
	if request.user.is_active:
		p = get_object_or_404(Parking, pk=pk)
		if request.user.is_superuser or request.user==p.user:			
			return render(request,'userprofile/parkinginfo.html',{'park':p,'orders':Order.objects.filter(parking=p)})

	raise Http404