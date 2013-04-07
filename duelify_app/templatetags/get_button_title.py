from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def get_button_title(ring, user):
    if ring.red.filter(pk=user.pk).exists() or ring.blue.filter(pk=user.pk).exists():
        return _(u'Continue discussion') + ' &raquo;'
    else:
        return _(u'View &amp; Vote') + ' &raquo;'