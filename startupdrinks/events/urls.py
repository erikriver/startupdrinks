from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

from .views import *

urlpatterns = patterns('',
    url(r'^$', EventDetail.as_view(), name="event_view"),
    url(r'^list$', EventUserList.as_view(), name="list"),
    url(r'^register$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^update$', update, name='update',),
    url(r'', include('social_auth.urls')),

    url(r'^admin$', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
