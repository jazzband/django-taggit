from django import template

register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__
