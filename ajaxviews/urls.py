from django.conf.urls import patterns, include, url

urlpatterns = patterns('ajaxviews.views',
	#login pages
	url(r'^userhome/$', 'userhome', name='ajax_get'),
	url(r'^login/$','ajax_login',name='ajax_login'),
	url(r'^parking/$','ajax_parkingdetails',name='parkingdetails'),
	url(r'^savebooking/$','ajax_savebooking',name='savebooking'),
)