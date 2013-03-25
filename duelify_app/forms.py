from duelify_app.models import Ring, DuelInvitation, Punch, Category
from django import forms
from django.forms.forms import Form
import re
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from duelify_app.admin import UserCreationForm

class FeedbackForm(Form):
    feedback        = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea_mandatory', 'placeholder': _(u"We will improve Duelify upon your feedback. :-)")}))


class ChooseCategoryForm(Form):
    def __init__(self, *args, **kwargs):
        super(ChooseCategoryForm, self).__init__(*args, **kwargs)        
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False 
    category = forms.ModelChoiceField(queryset='', label=_(u'Pick a category'))

class CategoryForm(forms.ModelForm):
    class Meta:        
        model = Category

class RingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RingForm, self).__init__(*args, **kwargs)        
        if self.instance.blue:
            self.fields['blue_invite'].initial = self.instance.blue
    blue_invite     = forms.EmailField(label=_(u'Your Opposition'), widget= forms.TextInput(attrs={'placeholder': _(u'Invite your friend or foe...'), 'class': 'placeholder_fix_css', 'autocomplete': 'off'}))
    
    class Meta:
        exclude = {'datetime'}
        model = Ring
        widgets = {
                'topic': forms.TextInput(  attrs={'placeholder': _(u'Enter the topic for discussion'), 'class': 'placeholder_fix_css', 'autocomplete': 'off'}),
             }
        
class PunchForm(forms.ModelForm):
    def __init__(self, is_edit, *args, **kwargs):
        super(PunchForm, self).__init__(*args, **kwargs)
        if is_edit:
            self.fields['discussion'].widget.attrs['placeholder'] = _(u'Continue the discussion according to your topic')
        else:        
            self.fields['discussion'].widget.attrs['placeholder'] = _(u'Start the discussion according to your topic')
    class Meta:
        exclude = {'speaker', 'ring', 'datetime', 'voters'}
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
        if is_accept_invite:            
            self.fields['email'].initial = email
            self.fields['email'].widget.attrs['readonly'] = True
            



        
