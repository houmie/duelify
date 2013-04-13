from django import template
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from duelify_app.models import Ring, Punch
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_score_for_user(user):    
    score = Ring.objects.filter(punch__voters=user).count() * 1    
    score = score + (Punch.objects.filter(speaker=user).aggregate(voter_count=Count('voters')))['voter_count'] * 5        
    score = score + Ring.objects.filter(Q(red=user)|Q(blue=user)).count() * 10        
    return score


@register.simple_tag    
def get_top10_users():
    top10 = get_user_model().objects.order_by('-score')[0:9]
    result = ''
    for top in top10:
        result = result + '{0}{1} {2}{3}{4}'.format('<li><a href="#">', top.get_full_name(), '</a>(', top.score, ')</li>')        
    return result
        