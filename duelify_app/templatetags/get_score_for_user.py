from django import template
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from duelify_app.models import Ring

register = template.Library()

@register.simple_tag
def get_score_for_user(user):
    score = 0
    votes = Ring.objects.filter(punch__voters=user)
    if votes:
        score = votes.count() * 2
    rings = Ring.objects.filter(Q(red=user)|Q(blue=user))
    if rings:
        score = score + rings.count() * 20
    return score
    

        