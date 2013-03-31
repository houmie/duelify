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


@register.simple_tag    
def get_top10_users():
    top10 = get_user_model().objects.order_by('-score')[0:9]
    result = ''
    for top in top10:
        result = result + '{0}{1} {2}{3}{4}'.format('<li><a href="#">', top.get_full_name(), '</a>(', top.score, ')</li>')        
    return result
        