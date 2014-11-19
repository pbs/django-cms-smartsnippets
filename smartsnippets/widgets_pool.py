from django.core.exceptions import ImproperlyConfigured
from cms.utils.django_load import load
from smartsnippets.exceptions import WidgetAlreadyRegistered, WidgetNotRegistered
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from models import SmartSnippetVariable
from collections import defaultdict


class WidgetPool(object):
    def __init__(self):
        self.widgets = {}
        self._settings = defaultdict(dict)
        self.discovered = False

    def discover_widgets(self):
        if self.discovered:
            return
        self.discovered = True
        load('widgets')

    def register_settings(self, namespace, settings_dict):
        self._settings[namespace].update(settings_dict)

    def unregister_settings(self, namespace, settings_keys=None):
        if settings_keys:
            for item in settings_keys:
                self._settings[namespace].pop(item, None)
        else:
            self._settings.pop(namespace, None)

    def register_widget(self, widget):
        if not issubclass(widget, SmartSnippetWidgetBase):
            raise ImproperlyConfigured(
                'Smartsnippets widgets must be subclasses of WidgetBase, %s is not.'
                % widget
            )
        widget_name = widget.__name__
        if widget_name in self.widgets:
            raise WidgetAlreadyRegistered(
                "Cannot register %s, a widget with this name (%s) is already "
                "retgistered." % (widget, widget_name)
            )

        widget.value = widget_name
        self.widgets[widget_name] = widget

    def unregister_widget(self, widget):
        widget_name = widget.__name__
        if widget_name not in self.widgets:
            raise WidgetNotRegistered(
                'The widget %s is not registered' % widget
            )
        del self.widgets[widget_name]

    def get_widget(self, name):
        self.discover_widgets()
        return self.widgets[name]

    def get_all_widgets(self, has_model=False, snippet=None):
        self.discover_widgets()
        widgets = [x for x in self.widgets.values() if x.model==SmartSnippetVariable]
        widgets.sort(key=lambda obj: unicode(obj.name))
        return widgets

    def get_settings(self, namespace, name=None):
        self.discover_widgets()
        if not name:
            return self._settings[namespace]
        return self._settings[namespace].get(name, None)

widget_pool = WidgetPool()
