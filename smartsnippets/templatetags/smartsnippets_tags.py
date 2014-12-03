from django import template
from collections import OrderedDict
from smartsnippets.widgets_pool import widget_pool


register = template.Library()

@register.simple_tag(takes_context=True)
def render_widget(context, var):
    request = context['request']
    return widget_pool.get_widget(var.widget)(var).render(request)


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
def get_item(iterable, key):
    dictionary = iterable
    if not hasattr(iterable, 'get'):
        try:
            dictionary = dict(enumerate(iterable))
        except (TypeError, ):
            return ''
    return (dictionary or {}).get(key, '')


@register.filter
def sortlist(list_to_sort):
    return sorted(list(list_to_sort))


@register.filter
def times(number):
    return range(number)


@register.filter
def split(string_to_split, delimiter=None):
    if not hasattr(string_to_split, 'split'):
        return []
    return (string_to_split or '').split(delimiter)


@register.assignment_tag
def as_dict(**kwargs):
    return OrderedDict(kwargs)
