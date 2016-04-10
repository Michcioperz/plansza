from django import template
from django.contrib.auth.models import User
from django.db.models import Q

from ..models import EventHour

register = template.Library()


@register.filter
def belongs_to(x, y):
    return x in y


@register.filter
def s_friends_in(x: User, y: EventHour):
    return User.objects.filter(hours=y).filter(Q(friend__friends=x.friend) | Q(pk=x.pk))


@register.filter
def placeholder_avatar(x: User):
    return "holder.js/150x150?size=50&random=yes&text=" + "".join(
        [y[0] for y in zip(x.get_full_name().title(), x.get_full_name().lower()) if y[0] != y[1]])
