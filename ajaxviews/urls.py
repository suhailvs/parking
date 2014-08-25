from django.conf.urls import patterns, include, url

urlpatterns = patterns('ajaxviews.views',
	#login pages
	url(r'^login/$','ajax_login',name='ajax_login'),
	url(r'^parking/$','ajax_parkingdetails',name='parkingdetails'),
)