from django import template
from collections import OrderedDict
from smartsnippets.widgets_pool import widget_pool

register = template.Library()

@register.simple_tag(takes_context=True)
def render_variable(context, var):
    request = context['request']
    return var.render(request)


@register.assignment_tag
def settings_value(what):
    return widget_pool.get_settings(*what.split('.', 1))


@register.filter
def sortdict(dict_to_sort):
    return OrderedDict(sorted(dict_to_sort.items()))


@register.filter
def get_item(dictionary, key):
    return (dictionary or {}).get(key, '')


@register.filter
def sortlist(list_to_sort):
    return sorted(list(list_to_sort))
