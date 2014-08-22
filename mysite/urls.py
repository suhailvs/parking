from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='guest/home.html'), name='home'),
    url(r'^p(\d+|all)/$', 'homepage.views.viewParking', name='parkings'),    
    url(r'^ajax/', include('ajaxviews.urls')),
    url(r'^admin/', include(admin.site.urls)),

	url(r"^account/", include("account.urls")),
)