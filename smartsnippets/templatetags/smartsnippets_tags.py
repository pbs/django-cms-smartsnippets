import json
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
def json_get_index(json_array, index):
    try:
        return json.loads(json_array)[index]
    except (TypeError, IndexError, ValueError, ):
        return ''


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
        context.get(n, empty)
        for n in name.split(sep or ',')]
    return result_items if len(result_items) > 1 else result_items[0]


def _select_operator(args):
    """
    The whole point of this function is to simulate multiple arguments
        for django filters.

    @args: string which represents the second argument of a filter; this is
    split into two parts:
        * first part will represent what operator will be returned
        * second part represents the name of the key/attribute which will
        be applied
    @returns operator by the name specified in @args; (currently supporting:
        'key' and 'attribute')
    """

    args_parts = args.rsplit(',', 1)
    func_by_args = lambda x: x
    if len(args_parts) != 2:
        return func_by_args

    what, which = args_parts
    if not which or what not in ('key', 'attribute'):
        return func_by_args

    if what == 'key':
        return lambda x: x.get(which, None)

    return lambda x: getattr(x, which, None)


@register.filter
def map_by(items, operator_args):
    """
        Applies map with specified operator over items. Used to return a
    list of specific key/attribute name from a list of dictionaries/objects.

    @operator_args: string with format `<operator_name>,<operator_argument>`
    Example operator_args: 'key,image' or 'attribute,color'
    Currently only 'key' and 'attribute' are supported.
    """
    return map(_select_operator(operator_args), items)


@register.filter
def exclude_empty(items, operator_args=None):
    """
        Applies filter with specified operator over items. Used to return
    items that are not considered empty. This function can exclude items
    from the list that have one specific key/attribute empty by using
    operator_args.

    @items: strings, integers, dictionaries or custom objects.
        Depending of what consideres a object to be empty the following
        operators are available: key, attribute.
    @operator_args: string with format `<operator_name>,<operator_argument>`.
        When operator_args is missing None will be used.
    Example operator_args: 'key,image' or 'attribute,color'
    """
    result_items = filter(None, items)
    if operator_args:
        result_items = filter(_select_operator(operator_args), result_items)
    return result_items
