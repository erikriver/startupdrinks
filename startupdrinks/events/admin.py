from django.contrib import admin
from django.forms.widgets import TextInput
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from .models import *

class SponsorsInline(admin.TabularInline):
    model = Sponsor
    classes = ('collapse closed',)
    inline_classes = ('collapse closed',)

class PhotoEventInline(admin.TabularInline):
    model = PhotoEvent
    classes = ('collapse open',)
    inline_classes = ('collapse open',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'place','active')
    list_filter = ('name','start')
    inlines = [PhotoEventInline, SponsorsInline]
    fields = ('name', 'city','start', 'end', 'place', 'active', 'open','site')
            
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        #obj.site = request.site
        obj.save()

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc' ,'address')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        map_fields.GeoLocationField: {'widget': TextInput(attrs={'readonly': 'readonly'})},
    }

admin.site.register(SiteSettings)
admin.site.register(Organizer)
admin.site.register(Testimonial)
admin.site.register(Profile)
admin.site.register(Event, EventAdmin)
admin.site.register(Places, PlacesAdmin)

admin.site.unregister(Group)
