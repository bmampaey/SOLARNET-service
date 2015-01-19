# To use, in template:
# {% load querystring %}
# {{ object|querystring }}

#See https://docs.djangoproject.com/en/1.7/howto/custom-template-tags/

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.http import QueryDict

register = template.Library()

@register.filter(needs_autoescape=True)
def querystring(value, autoescape=None):
	"""Display a query string as an html list"""
	
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	
	q = QueryDict(value)
	result = "<ul>\n"
	for key, val in q.iterlists():
		if not key.startswith("selectItem"):
			result += "<li>{key}: {values}</li>\n".format(key=esc(key), values= esc(", ".join(val)))
	result += "</ul>"
	return mark_safe(result)

register.filter('querystring', querystring)