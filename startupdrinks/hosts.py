from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'startupdrinks\.mx', settings.ROOT_URLCONF, name='www'),
    host(r'(?P<subdomain>\w+)', 'startupdrinks.events.urls', name='wildcard'),
)