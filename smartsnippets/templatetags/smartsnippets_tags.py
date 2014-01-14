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


@register.inclusion_tag('smartsnippets/widgets/colorfield/widget.html',
                        takes_context=True)
def show_color_field(context, fieldname, fieldvalue):
    return {
        'field': {
            'name':fieldname,
            'value':fieldvalue
            },
        'STATIC_URL' : context.get('STATIC_URL')
        }

@register.inclusion_tag('smartsnippets/widgets/imagefield/widget.html',
                        takes_context=True)
def show_image_field(context, fieldname, fieldvalue):
    return {
        'field': {
            'name':fieldname,
            'value':fieldvalue
            },
        'optional_field' : True,
        'STATIC_URL' : context.get('STATIC_URL')
        }

@register.inclusion_tag('smartsnippets/widgets/textfield/widget.html',
                        takes_context=True)
def show_text_field(context, fieldname, fieldvalue):
    return {
        'field': {
            'name':fieldname,
            'value':fieldvalue
            },
        }