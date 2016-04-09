from django import template

register = template.Library()


@register.filter
def belongs_to(x, y):
    return x in y
