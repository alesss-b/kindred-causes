from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_attr(obj, attr):
    attribute = getattr(obj, attr, '')

    print(type(attribute))

    if type(attribute) is User:
        return attribute.get_full_name()

    return attribute
