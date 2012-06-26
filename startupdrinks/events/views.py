from uuid import uuid4
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from django.views.generic import ListView, DetailView, TemplateView, CreateView

from social_auth.signals import pre_update

from .models import *
from .forms import *

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
    template_name = "list.html"
    
    def get_queryset(self):
        host = self.request.get_host()
        self.site = get_object_or_404(Site, domain__iexact=host)
        events = list(Event.objects.filter(active=True, site=self.site)[:1])
        if events:
            event = events[0]
            return event.attendees.all()
            
    def get_context_data(self, **kwargs):
        context = super(EventUserList, self).get_context_data(**kwargs)
        context['site_settings'] = self.site.sitesettings
        return context
    
def user_update(sender, user, response, details, **kwargs):
    network = sender.name
    profile, created = Profile.objects.get_or_create(user=user)
    profile.fullname = details.get('fullname','')
    profile.network_id = response['id']
    profile.network = network
    
    if network == 'facebook':
        profile.network_url = response['link']
        profile.photo_url = 'https://graph.facebook.com/'+response['id']+'/picture'
    
    if network == 'twitter':
        profile.network_url = 'https://twitter.com/#!/'+response['screen_name']
        profile.photo_url = response['profile_image_url']    
        
    if not user.email:
        user.email = details.get('email','')
    
    user.save()
    profile.save()
    return True

pre_update.connect(user_update)


#@login_required
def update(request, template_name="update.html"):
    data = {}
    profile = None
    
    if request.user.is_authenticated():
        profile = request.user.get_profile()    
        data = {
            'email':    profile.user.email,
            'fullname': profile.fullname,
            'bio':      profile.bio,
            'expect':   profile.expect
        }

    form = UserForm(request.POST or None, initial=data)
    
    host = request.get_host()
    site = get_object_or_404(Site, domain__iexact=host)
    
    if request.method == 'POST':
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            
            if profile is None:
                username = uuid4().get_hex()[:8]
                user = User.objects.create_user(username=username, email=email)
                profile, created = Profile.objects.get_or_create(user=user)
            
            profile.user.email = email
            profile.fullname = form.cleaned_data.get('fullname')
            profile.kind = form.cleaned_data.get('kind')
            profile.bio = form.cleaned_data.get('bio')
            profile.expect = form.cleaned_data.get('expect')
            
            events = list(Event.objects.filter(active=True, site=site)[:1])
            profile.site = site
            
            profile.user.save()
            profile.save()
            
            if events:
                event = events[0]
                event.attendees.add(profile)
                
                #verificar si es actializacion o nuevo registro
                activity = AttendActivity.objects.create(actor=profile.user, action='registered', target=event)
                activity.save()
            
            logout(request)
            return HttpResponseRedirect('/')

    return render(request, template_name, {"form": form,"site_settings": site.sitesettings })
    