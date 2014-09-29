from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail,EmailMultiAlternatives
# Create your views here.
from django.contrib import messages
from django.conf import settings


from django.template import Context 
from django.template.loader import render_to_string

def send_html_email(template_name,params,subj,to):
	ctx = Context(params)
	text_content = render_to_string('customemails/{0}.txt'.format(template_name), ctx)
	html_content = render_to_string('customemails/{0}.html'.format(template_name), ctx)
	email = EmailMultiAlternatives(subj, text_content,settings.DEFAULT_FROM_EMAIL,to)
	email.attach_alternative(html_content, "text/html")	
	email.send()

def contactmail(request):
	if request.method=='POST':
		msg=request.POST.get('message')
		name=request.POST.get('name')
		phone=request.POST.get('phone')
		email=request.POST.get('email')
		if len(msg)<20 or name=='' or phone=='' or email=='':
			messages.error(request, 'All fields are required. and message must have atleast 20chars.')
			return HttpResponseRedirect(reverse('home')+'#contact')
		
		ctx=dict(name=name,phone=phone,email=email,msg=msg)
		send_html_email(
			template_name='contactmail',
			params=ctx,
			subj="A User send a message through flexlot contact us page",
			to=[settings.CONTACT_US_EMAIL])
		return HttpResponseRedirect(reverse('contact_mail')+'?flag=success')
		
	if 'flag' in request.GET and request.GET['flag']=='success':return render(request,'customemails/success.html')
	raise Http404



