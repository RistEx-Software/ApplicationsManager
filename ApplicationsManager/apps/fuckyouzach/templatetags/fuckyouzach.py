from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='getname')
def getname(value):
	if not isinstance(value, User):
		raise AttributeError("Must be a `User` object")
		
	if value.first_name and value.last_name:
		return value.get_full_name()
	else:
		return value.username
