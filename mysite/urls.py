from django.urls import include, re_path, path
from django.views.generic import TemplateView
from django.contrib import admin
from homepage.views import ShareParkingStuff,CustSignupView,MyHome,FindParkings,CustLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from homepage import views as homepageviews
from payments import views as paymentviews

urlpatterns = [
    # Examples:url(r'^$', TemplateView.as_view(template_name='guest/home.html'), name='home'),    
    re_path(r'^$', MyHome.as_view(), name='home'),
    re_path(r'^share/$', login_required(ShareParkingStuff.as_view(),login_url='/account/login/'), name='shareparking'),
    #url(r'^edit/(\d+)/$', login_required(ShareParkingStuff.as_view(),login_url='/account/login/'), name='editparking'),
    re_path(r'^find/$', FindParkings.as_view(), name='findparking'),
    re_path(r'^p/(\d+)/$', homepageviews.parking_info, name='parkingInfo'),
    re_path(r'^driverinfo/$', homepageviews.add_driver_details, name='driver_info'),


    re_path(r'^ajax/', include('ajaxviews.urls')),
    re_path(r'^paypal/', include('paypal.standard.ipn.urls')),
    re_path(r'^admin/remove_inactive_orders/$', paymentviews.remove_inactive_orders, name='removeOrders'),
    re_path(r'^admin/viewparkings/$', homepageviews.adminhome, name='admin_view_parking'),
    path('admin/', admin.site.urls),
    

    re_path(r"^account/signup/$", CustSignupView.as_view(), name="account_signup"),
    re_path(r"^account/login/$", CustLoginView.as_view(), name="account_login"),    
	re_path(r"^account/", include("account.urls")),
     re_path(r'^payment/ask_for_money/$', paymentviews.frm_paypal, name='ask_for_money'),
    re_path(r'^payment/(success|cancel)/$', paymentviews.paypal_redirect_pages, name='paypal_redirect_pages'),
]
# for openshift
#urlpatterns += staticfiles_urlpatterns()


# handler404 = 'mysite.views.my_custom_404_view'
# handler500 = 'mysite.views.my_custom_404_view'
# handler403 = 'mysite.views.my_custom_404_view'