from django import template
from collections import OrderedDict
from smartsnippets.widgets_pool import widget_pool
from datetime import datetime


register = template.Library()


@register.simple_tag(takes_context=True)
def render_widget(context, var):
    request = context['request']
    widget_cls = widget_pool.get_widget(var.widget)
    widget_obj = widget_cls(var)
    return widget_obj.render(request, context)


@register.simple_tag(takes_context=True)
def render_variable(context, var):
    request = context['request']
    return var.render(request, context)


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


@register.assignment_tag
def current_timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")


@register.assignment_tag(takes_context=True)
def from_context(context, name, sep=None, empty=None):
    result_items = [
        (context.get(n, None) or empty)
        for n in name.split(sep or ',')]
    return result_items if len(result_items) > 1 else result_items[0]


def _by_args(args):
    func_by_args = lambda x: x
    args = args.rsplit(',', 1)
    if len(args) != 2:
        return func_by_args

    what, which = args[0], args[1]
    if not which or what not in ('key', 'attribute'):
        return func_by_args

    if what == 'key':
        return lambda x: x.get(which, None)

    return lambda x: getattr(x, which, None)


@register.filter
def map_by(items, args):
    return map(_by_args(args), items)


@register.filter
def exclude_empty(items, args=None):
    return filter(_by_args(args) if args else None, items)
