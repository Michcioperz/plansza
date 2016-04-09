from django import template

from ..models import Friend

register = template.Library()


@register.filter
def belongs_to(x, y):
    return x in y


@register.filter
def s_friends_in(x, y):
    return Friend.objects.filter()
