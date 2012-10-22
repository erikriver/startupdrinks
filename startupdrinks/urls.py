from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    #    url(r'^admin/', include(admin.site.urls)),
    #    (r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
