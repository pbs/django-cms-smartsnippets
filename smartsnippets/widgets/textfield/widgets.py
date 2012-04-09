from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase

class TextField(SmartSnippetWidgetBase):
    name = 'Text Field'

widget_pool.register_widget(TextField)