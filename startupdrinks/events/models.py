from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from sorl.thumbnail import ImageField
from django_google_maps import fields as map_fields

THEME_CHOICES = (
        ('red',    _('Red')),
        ('green',  _('Green')),
        ('blue',    _('Blue')),
        ('brown',    _('Brown')),
)

class SiteSettings(models.Model):
    site    = models.OneToOneField(Site,  primary_key=True)
    name    = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    logo    = ImageField(upload_to='logos', blank=True)
    fb_user = models.URLField(blank=True)
    fb_page = models.URLField(blank=True)
    #flickr_page = models.URLField(blank=True)
    twitter_user = models.CharField(_('Twitter User'), max_length=50, blank=True, null=True)
    twitter_ht   = models.CharField(_('Twitter Hashtag'), max_length=50, blank=True, null=True)
    theme   = models.CharField(_('Theme'), max_length=50, choices=THEME_CHOICES, default='brown')
    
    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Sites Setting")
        ordering = ['name']
        
    def __unicode__(self):
        return u"%s" % self.name

KIND_CHOICES = (
        ('entrepreneur',_('Emprendedor')),
        ('startup',     _('Startup')),
        ('geek',        _('Geek')),
        ('coach',       _('Coach/Mentor')),
        ('investor',    _('Inversionista')),
        ('gossip',      _('Chismoso')),
        ('joker',       _('Comodin')),
)
    
class Profile(models.Model):
    
    user = models.OneToOneField(User)
    fullname = models.CharField(_('Full name'), max_length=100, null=True, blank=True)
    bio = models.TextField(_('Description'), blank=True)
    expect = models.TextField(_('Expect'), blank=True)
    kind   = models.CharField(_('Profile'), max_length=50, choices=KIND_CHOICES, default='entrepreneur')
    network = models.CharField(max_length=255, blank=True, null=True)
    network_id = models.CharField(max_length=255, blank=True, null=True)
    network_url = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.BooleanField(_('Organizador'))
    site = models.ForeignKey(Site, default=1,blank=True)
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ['fullname']

    def get_kind(self):
        data = dict(KIND_CHOICES)
        return data[self.kind]

    @property
    def email(self):
        return self.user.email
    
    
class Testimonial(models.Model):
    text    = models.TextField(_('Text'), blank=True)
    author  = models.CharField(_('Author'), max_length=255, blank=True, null=True)
    site    = models.ForeignKey(Site, blank=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['author']
    
    
class Places(models.Model):
    name    = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    desc    = models.TextField(_('Description'), blank=True)
    image   = ImageField(upload_to='places', blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(blank=True)
    site    = models.ForeignKey(Site, blank=True)
    
    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['name',]

    def __unicode__(self):
        return u"%s" % self.name
        
class Organizer(models.Model):
    name = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True)
    web_page    = models.URLField(blank=True)
    facebook    = models.URLField(blank=True)
    twitter     = models.URLField(blank=True)
    linkedin    = models.URLField(blank=True)
    image = ImageField(upload_to='sponsors')
    event = models.ForeignKey('Event', related_name='organizers')
    site    = models.ForeignKey(Site, blank=True)
    
    class Meta:
        verbose_name = _("Organizer")
        verbose_name_plural = _("Organizers")
        ordering = ['name']
    
    def __unicode__(self):
        return u"%s" % self.name


class Sponsor(models.Model):
    name = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True)
    link = models.URLField()
    image = ImageField(upload_to='sponsors')
    event= models.ForeignKey('Event', related_name='sponsors')

    def __unicode__(self):
        return u"%s" % self.name


class Event(models.Model):
    name    = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    city    = models.CharField(_('Ciudad'), max_length=100, blank=True, null=True)
    owner   = models.ForeignKey(User)
    place   = models.ForeignKey(Places)
    start   = models.DateTimeField(_('Inicio'))
    end     = models.DateTimeField(_('Fin'))
    open    = models.BooleanField(_('Abierto'))
    active  = models.BooleanField(_('Activo'))
    attendees = models.ManyToManyField(Profile, blank=True, null=True, related_name='attend_events')
    site    = models.ForeignKey(Site)
        
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('start',)

    def __unicode__(self):
        return u"%s" % self.name

class AttendActivity(models.Model):
    actor   = models.ForeignKey(User)
    action  = models.CharField(max_length=255, blank=True, null=True)
    date    = models.DateTimeField(auto_now_add=True)
    target  = models.ForeignKey(Event)

class PhotoEvent(models.Model):
    event= models.ForeignKey(Event, related_name='photos')
    name = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True)
    image = ImageField(upload_to='carousel')

    def __unicode__(self):
        return u"%s" % self.name

