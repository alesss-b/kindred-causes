from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_attr(obj, attr):
    print(obj, attr)

    if '.' in attr and type(attr) == str:
        attribute = get_attr(obj, attr.split('.')[0])
        return get_attr(attribute, attr.split('.')[1])

    attribute = getattr(obj, attr, '')

    print(type(attribute))
    print(attribute)

    if type(attribute) is User:
        print("User")
        return attribute.get_full_name()

    elif callable(attribute):
        print("Callable")
        return attribute()


    return attribute
