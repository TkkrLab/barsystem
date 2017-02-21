from django import template
from django.template.defaultfilters import floatformat
import barsystem.functions

register = template.Library()

@register.filter
def money_display(value, *args, **kwargs):
	return barsystem.functions.money_display(value)