from django.urls import include, re_path
from ajaxviews import views

urlpatterns = [
	#login pages
	re_path(r'^userhome/$', views.userhome, name='ajax_home'),
	#url(r'^login/$','ajax_login',name='ajax_login'),
	re_path(r'^parking/availability$',views.ajax_parkingavailability,name='parkingavailability'),	
	
	re_path(r'^parking/$',views.ajax_parkingdetails,name='parkingdetails'),
	re_path(r'^savebooking/$',views.ajax_savebooking,name='savebooking'),
	re_path(r'^edit/(\d+)/$',views.editparking, name='editparking'),
]