from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def render_variable(context, var):
    request = context['request']
    return var.render(request)