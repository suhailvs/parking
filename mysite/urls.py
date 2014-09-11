from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from homepage.views import ShareParkingStuff,CustSignupView,MyHome
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:url(r'^$', TemplateView.as_view(template_name='guest/home.html'), name='home'),    
    url(r'^$', MyHome.as_view(), name='home'),
    url(r'^share/$', login_required(ShareParkingStuff.as_view(),login_url='/account/login/'), name='shareparking'),
    url(r'^edit/(\d+)/$', login_required(ShareParkingStuff.as_view(),login_url='/account/login/'), name='editparking'),
    url(r'^find/$', 'homepage.views.FindParking', name='findparking'),
    #url(r'^user/$', 'homepage.views.userpage', name='users'),
    #url(r'^user/(\w+)/$', 'homepage.views.userpage', name='users'),

    url(r'^ajax/', include('ajaxviews.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^account/signup/$", CustSignupView.as_view(), name="account_signup"),
	url(r"^account/", include("account.urls")),
)
# for openshift
#urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('payments.views',    
    url(r'^payment/ask_for_money/$', 'frm_paypal', name='ask_for_money'),
    url(r'^payment/(success|cancel)/$', 'paypal_redirect_pages', name='paypal_redirect_pages'),
    #url(r'^cancel/$', 'frm_paypal', name='ask_for_money'),
    #url(r'^payment/$','asks_for_money'),
)