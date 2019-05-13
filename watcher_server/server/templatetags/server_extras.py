from django import template

register = template.Library()

@register.filter
def addstr(first, second):
    return str(first) + str(second)