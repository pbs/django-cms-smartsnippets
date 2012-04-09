from django.core.exceptions import ImproperlyConfigured
from utils.widgets_load import load
from smartsnippets.exceptions import WidgetAlreadyRegistered, WidgetNotRegistered
from smartsnippets.widgets_base import SmartSnippetWidgetBase


class WidgetPool(object):
    def __init__(self):
        self.widgets = {}
        self.discovered = False
        
    def discover_widgets(self):
        if self.discovered:
            return
        self.discovered = True
        load('widgets')
        
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
    
    def get_all_widgets(self, snippet=None):
        self.discover_widgets()
        widgets = self.widgets.values()
        widgets.sort(key=lambda obj: unicode(obj.name))
        return widgets

widget_pool = WidgetPool()