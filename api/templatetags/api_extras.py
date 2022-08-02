from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def replace(value, arg):
    return value.replace(arg, "")


@register.filter
def remove_line_breaks(value):
    value = value.replace('"', '\"')
    value = value.replace("'", "\\'")
    return value.replace("\n", " ")


@register.filter
def get_color(lst, val):
    return lst.get(val, 'gray-700')


@register.filter
def get_array_element(lst, val, default=''):
    return lst.get(val, default)
