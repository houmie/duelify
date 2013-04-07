from duelify_app.models import Ring, DuelInvitation, Punch, Category, SIDES,\
    RULES, SIDES_C
from django import forms
from django.forms.forms import Form
import re
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from duelify_app.admin import UserCreationForm
from django.template.defaultfilters import striptags
from django.contrib.auth.forms import AuthenticationForm


class AjaxBaseForm(forms.BaseForm):
    def errors_as_json(self, strip_tags=False):
        error_summary = {}
        errors = {}
        for error in self.errors.iteritems():
            errors.update({error[0] : unicode(striptags(error[1]) \
                if strip_tags else error[1])})
        error_summary.update({'errors' : errors })
        return error_summary


class AjaxModelForm(AjaxBaseForm, forms.ModelForm):
    """Ajax Form class for ModelForms"""
    pass


class AjaxForm(AjaxBaseForm, forms.Form):
    """Ajax Form class for Forms"""
    pass

class AjaxLoginForm(AjaxBaseForm, AuthenticationForm):
    pass
    

class FeedbackForm(Form):
    feedback        = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea_mandatory', 'placeholder': _(u"We will improve Duelify upon your feedback. :-)")}))


class ChooseCategoryForm(Form):
    def __init__(self, *args, **kwargs):
        super(ChooseCategoryForm, self).__init__(*args, **kwargs)        
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False 
    category = forms.ModelChoiceField(queryset='', label=_(u'Pick a category'))
    show_open_topics = forms.BooleanField(label=_(u'Show Only Open Topics'), required=False)

class CategoryForm(forms.ModelForm):
    class Meta:        
        model = Category

class RingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RingForm, self).__init__(*args, **kwargs)        
#        if self.instance.blue:
#            self.fields['blue_invite'].initial = self.instance.blue
        self.fields['category'].widget.attrs['class'] = 'big-input'
        self.fields['blue_invite'].required = False
        #self.fields['pick_side'].widget.attrs['class'] = 'big-input'
            
    blue_invite = forms.EmailField(label=_(u'Email of your opponent - OR - Leave empty as open topic'), widget= forms.TextInput(attrs={'placeholder': _(u'Invite your friend or foe'), 'class': 'placeholder_fix_css big-input', 'autocomplete': 'off'}))
    #pick_side   = forms.ChoiceField(choices=SIDES, label=_(u'Do you agree or disagree with the topic?'))
    class Meta:
        exclude = {'datetime'}
        model = Ring
        widgets = {
                'topic': forms.TextInput(  attrs={'placeholder': _(u'Enter the topic for discussion'), 'class': 'placeholder_fix_css big-input', 'autocomplete': 'off'}),
                'rule': forms.RadioSelect(),                
             }
        
class PunchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_new = kwargs.pop('is_new', None)
        #is_continue = kwargs.pop('is_continue', None)
        super(PunchForm, self).__init__(*args, **kwargs)        
        self.fields['discussion'].widget.attrs['placeholder'] = _(u'Express your opinion according to given topic')
        self.fields['side'].widget.attrs['class'] = 'big-input'
        if self.instance.side:
            self.fields['side'].required = False
        #self.fields['side'].widget.empty_label = None         
        
        if is_new:
            self.fields['side'].label = _(u'Do you agree or disagree with your topic?')
        #if is_continue:
        #    self.fields['side'].widget.attrs['class'] = 'hidden'
        
    class Meta:
        exclude = {'ring', 'datetime', 'voters', 'speaker'}
        model = Punch
        widgets = {
                'discussion': forms.Textarea(  attrs={'class': 'discussion placeholder_fix_css', 'autocomplete': 'off'}),
                
             }

#class FriendsInviteForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super(FriendsInviteForm, self).__init__(*args, **kwargs)
#        self.fields['name'].widget.attrs['class'] = 'demo-input'
#        self.fields['email'].widget.attrs['class'] = 'demo-input'
#        self.fields['name'].widget.attrs['autocomplete'] = 'off'
#        self.fields['email'].widget.attrs['autocomplete'] = 'off'
#    
#    def clean_email(self):
#        email = self.cleaned_data['email']
#        users = User.objects.filter(email=email)
#        if users.count() > 0:
#            raise forms.ValidationError(_(u"This email is already registered in the system, please select another."))
#        return email
#    
#    class Meta:
#        model = FriendInvitation
#        fields = {'name', 'email', 'ring'}


#class DuelInviteForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super(DuelInviteForm, self).__init__(*args, **kwargs)        
#        self.fields['email'].widget.attrs['class'] = 'demo-input'        
#        self.fields['email'].widget.attrs['autocomplete'] = 'off'
#    
##    def clean_email(self):
##        email = self.cleaned_data['email']
##        users = User.objects.filter(email=email)
##        if users.count() > 0:
##            raise forms.ValidationError(_(u"This email is already registered in the system, please select another."))
##        return email
#    
#    class Meta:
#        model = DuelInvitation
#        fields = {'email', 'ring'}

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):        
        email = kwargs.pop('_email', None)
        is_accept_invite = kwargs.pop('is_accept_invite', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = _(u'Email')        
        self.fields['date_of_birth'].widget.attrs['placeholder'] = _(u'To adjust age restricted content')
        self.fields['password2'].widget.attrs['placeholder'] = _(u'Type in the same password again')
        self.fields['date_of_birth'].widget.attrs['class'] = 'date_picker big-input'
        self.fields['email'].widget.attrs['class'] = 'big-input'
        self.fields['password1'].widget.attrs['class'] = 'big-input'
        self.fields['password2'].widget.attrs['class'] = 'big-input'
        self.fields['first_name'].widget.attrs['class'] = 'big-input'
        self.fields['last_name'].widget.attrs['class'] = 'big-input'
        if is_accept_invite:            
            self.fields['email'].initial = email
            self.fields['email'].widget.attrs['readonly'] = True
            



        
