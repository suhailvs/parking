from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
# Create your views here.
from django.contrib import messages
from django.conf import settings

def contactmail(request):
	if request.method=='POST':
		msg=request.POST.get('message')
		name=request.POST.get('name')
		phone=request.POST.get('phone')
		email=request.POST.get('email')
		if len(msg)<20 or name=='' or phone=='' or email=='':
			messages.error(request, 'All fields are required. and message must have atleast 20chars.')
			return HttpResponseRedirect(reverse('home')+'#contact')

			return render(request,'home.html',{'error':'All fields are required and message must have atleast 20chars'})
		message="""
		User Details
		------------
		Name: {0}
		Phone: {1}
		email: {2}

		Message
		------------
		{3}
		""".format(name,phone,email,msg)
		send_mail("A User send a message through flexlot contact us page", 
			message, settings.DEFAULT_FROM_EMAIL,[settings.CONTACT_US_EMAIL], fail_silently=False)#['info@flexspot.co']
			
		return HttpResponseRedirect(reverse('contact_mail')+'?flag=success')
		
	if 'flag' in request.GET and request.GET['flag']=='success':return render(request,'customemails/success.html')
	raise Http404
