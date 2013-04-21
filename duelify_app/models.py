from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.template.loader import get_template
from django.template.context import Context
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google
from tinymce.models import HTMLField


def validate_min_100(value):
    if value.__len__()  < 100:
        raise ValidationError(u'Only %s characters? - please express your opinion in more than 100 characters' % value.__len__())

SIDES = (        
            ('blue',        _(u'Agree')),
            ('red',         _(u'Disagree')),
        )

SIDES_C = (        
            ('blue',        _(u'Blue (agree)')),
            ('red',         _(u'Red (disagree)')),
        )

RULES = (
            ('public',    _(u'Open to anyone to participate')),
            ('personal',  _(u'Limited to only you and your invitee')),
        )

class Category(models.Model):
    category            = models.CharField(_(u'Category'), max_length=35)    
    def __unicode__(self):
        return self.category

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

class Ring(models.Model):
    category        = models.ForeignKey(Category, blank=True, null=True)
    topic           = models.CharField(_(u'Topic'), max_length=50)
    slug            = models.SlugField()
    red             = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='red_users' , blank=True, null=True)
    blue            = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blue_users', blank=True, null=True)
    datetime        = models.DateTimeField()
    rule            = models.CharField(_(u'Who can vote?'), max_length=8, choices=RULES, default='public')
        
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.topic)
        super(Ring, self).save(*args, **kwargs)
        
    
    def __unicode__(self):
        return self.topic
    class Meta:
        verbose_name = _(u'Ring')
        verbose_name_plural = _(u'Rings')


class Punch(models.Model):
    ring            = models.ForeignKey(Ring)
    speaker         = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='speaker')
    side            = models.CharField(max_length=4, choices=SIDES_C, default='blue', verbose_name=_("On which side are you?"), blank=False)
    discussion      = HTMLField(_(u'Express your opinion'))#, validators=[validate_min_100])
    datetime        = models.DateTimeField()
    voters          = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name= _("Voters"), null=True, blank=True)
    
    def save(self, *args, **kwargs):    
        super(Punch, self).save(*args, **kwargs) # Call the "real" save() method.
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
    
    def get_votes(self):
        return self.voters.count()
    
    def __unicode__(self):        
        return u'%s' % (self.datetime) 
    class Meta:
        verbose_name = _(u'Punch')
        verbose_name_plural = _(u'Punches')



class DuelInvitation(models.Model):    
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    ring = models.ForeignKey(Ring)
    
    def __unicode__(self):
        return u'%s, %s' % (self.sender.last_name, self.email)    

    def send(self):
        subject = _(u'Invitation to a Duel')
        link = '%s/duel/accept/%s/' % (settings.SITE_HOST, self.code)
        template = get_template('registration/invitation_email.txt')
        context = Context({'link': link, 'sender': self.sender.get_full_name(), 'topic':self.ring.topic})
        message = template.render(context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
        
        



class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, date_of_birth=None, password=None, location=None, browser=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
#        if not first_name:
#            raise ValueError('Users must have an first name')
#        
#        if not last_name:
#            raise ValueError('Users must have an last name')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth or None,
            first_name=first_name or '',
            last_name=last_name or '',
            location=location or '',
            browser=browser or ''
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, location=None, browser=None, date_of_birth=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        
        if not email:
            raise ValueError('Users must have an email address')
        
        if not first_name:
            raise ValueError('Users must have an first name')
        
        if not last_name:
            raise ValueError('Users must have an last name')
        
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
            location=location,
            browser=browser
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
  
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, db_index=True,)
    date_of_birth = models.DateField(blank=True, null=True)    
    location = models.CharField(max_length=250, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)   
    score = models.PositiveIntegerField(default=0) 
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `Duelify_app`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin    