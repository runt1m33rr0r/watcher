from django import template


register = template.Library()

@register.filter
def concat(first, second):
    return str(first) + str(second)