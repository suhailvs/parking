from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from homepage.views import NewParking
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='guest/home.html'), name='home'),
    url(r'^p/(\d+|all|my)/$', 'homepage.views.viewParking', name='parkings'),   
    url(r'^p/new/$', login_required(NewParking.as_view(),login_url='/account/login/'), name='list_parking'),

    url(r'^ajax/', include('ajaxviews.urls')),
    url(r'^admin/', include(admin.site.urls)),

	url(r"^account/", include("account.urls")),
)
