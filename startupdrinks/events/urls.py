from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = patterns('',
    url(r'^$', EventDetail.as_view(), name="event_view"),
    url(r'^list$', EventUserList.as_view(), name="list"),
    url(r'^register$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^update$', update, name='update',),
    url(r'', include('social_auth.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )