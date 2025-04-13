from django.template import Library
from decimal import Decimal as D


register = Library()


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * int(arg)

@register.filter(name='divide')
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter(name='true_yes')
def true_yes(value):
    return "Yes" if value == True else "No"


@register.filter(name='clean', is_safe=True)
def clean(value, symbols):
    for s in symbols.split(","):
        replaced = value.replace(s, " ")
    return replaced

@register.filter(name='capword', is_safe=True)
def capword(value):
    return value.title()

@register.filter(name='startswith', is_safe=True)
def startswith(field, value):
    return field.startswith(value)

@register.filter(name='has_perm', is_safe=True)
def has_perm(user, perm):
    return user.has_perm(perm)

@register.filter(name='two_d', is_safe=True)
def two_d(value):
    # return round(value,2)
    return "{:,.2f}".format(D(value))