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


@register.filter
def placeholder_avatar(x: User):
    return "holder.js/150x150?text=" + "".join(
        [y[0] for y in zip(x.get_full_name().capitalize(), x.get_full_name().lower()) if y[0] != y[1]])
