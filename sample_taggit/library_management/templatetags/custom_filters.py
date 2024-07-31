from django import template

register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def order_tags(tags):
    return tags.order_by("name")
