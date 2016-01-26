from django import template
from django.template.defaultfilters import floatformat
import barsystem_base.functions

register = template.Library()

@register.filter
def money_display(value, *args, **kwargs):
	return barsystem_base.functions.money_display(value)