from django.conf import settings
from django.conf.urls.defaults import *
from .views import *

urlpatterns = patterns('',
    url(r'^$', EventDetail.as_view(), name="event_view"),
    url(r'^users/$', EventUserList.as_view(), name="event_view"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )