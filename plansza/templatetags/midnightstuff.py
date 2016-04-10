from django import template
from django.contrib.auth.models import User

from ..models import EventHour

register = template.Library()


@register.filter
def belongs_to(x, y):
    return x in y


@register.filter
def s_friends_in(x: User, y: EventHour):
    return User.objects.filter(friend__friends=x.friend, hours=y)
