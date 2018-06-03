from django import template
import dateutil

register = template.Library()

@register.filter(name='iso8601_to_date')
def iso8601_to_date(value):
    return dateutil.parser.parse(value)