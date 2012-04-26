from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from .models import *

class EventDetail(DetailView):
    model = Event
    template_name = "detail.html"
    context_object_name = "event"
    site = None
    
    def get_object(self):
        host = self.request.get_host()
        self.site = get_object_or_404(Site, domain__iexact=host)
        events = list(Event.objects.filter(active=True, site=self.site)[:1])
        if events:
          return events[0]
        return None
        
    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['site_settings'] = self.site.sitesettings
        context['photos'] = self.object.photos.all()
        context['sponsors'] = self.object.sponsors.all()
        context['testimonials'] = Testimonial.objects.filter(site=self.site)
        context['organizers'] = Organizer.objects.filter(site=self.site)
        return context
    
class EventUserList(ListView):
    model = Profile

