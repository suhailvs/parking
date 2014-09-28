from django.conf.urls import patterns, include, url

urlpatterns = patterns('customemails.views',
	#login pages
	url(r'^contact/$', 'contactmail', name='contact_mail'),
)