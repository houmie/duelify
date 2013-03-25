from django import template
from django.contrib.auth import get_user_model

register = template.Library()

@register.simple_tag
def get_votes_for_punch(punch, user):
    if punch.voters.filter(pk=user.pk).count() > 0:
        return 'btn-success'
    else:
        return ''