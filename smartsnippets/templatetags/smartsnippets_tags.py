from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag(takes_context=True)
def render_variable(context, var):
    request = context['request']
    return var.render(request)

@register.filter
@stringfilter
def underscore2space(str):
    return str.replace("_", " ")