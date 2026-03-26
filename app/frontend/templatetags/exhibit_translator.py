from django import template
from django.utils import translation

register = template.Library()

@register.filter(name="get_description")
def get_description(value, arg):
    if arg == 'en':
        return value.description_en
    else:
        return value.description_it

@register.filter(name="get_excerpt")
def get_excerpt(value, arg):
    if arg == 'en':
        return value.excerpt_en
    else:
        return value.excerpt_it
