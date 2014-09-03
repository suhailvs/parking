from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from homepage.views import ShareParking
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='guest/home.html'), name='home'),    
    url(r'^share/$', login_required(ShareParking.as_view(),login_url='/account/login/'), name='shareparking'),
    url(r'^find/$', 'homepage.views.FindParking', name='findparking'),
    url(r'^user/$', 'homepage.views.userpage', name='users'),
    url(r'^user/(\w+)/$', 'homepage.views.userpage', name='users'),

    url(r'^ajax/', include('ajaxviews.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r"^account/signup/$", CustSignupView.as_view(), name="account_signup"),
	url(r"^account/", include("account.urls")),
)
# for openshift
#urlpatterns += staticfiles_urlpatterns()