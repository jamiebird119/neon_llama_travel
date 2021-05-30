from django import template



register = template.Library()

@register.filter(name="lower_replace")
def lower_replace(value):
    """Removes all values of arg from the given string"""
    return value.lower().replace(" ","_")