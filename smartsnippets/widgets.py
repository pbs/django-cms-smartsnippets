from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from .models import DropDownVariable
import collections
import json


class TextField(SmartSnippetWidgetBase):
    name = 'Text Field'
    template = 'smartsnippets/widgets/textfield/widget.html'


class TextAreaField(SmartSnippetWidgetBase):
    name = 'TextArea Field'
    template = 'smartsnippets/widgets/textareafield/widget.html'


class DropDownField(SmartSnippetWidgetBase):
    name = 'DropDown Field'
    model = DropDownVariable
    template = 'smartsnippets/widgets/dropdownfield/widget.html'

class SwitcherField(SmartSnippetWidgetBase):
    name = 'Switcher Field'
    template = 'smartsnippets/widgets/switcherfield/widget.html'


class URLField(SmartSnippetWidgetBase):
    name = 'URL Field'
    template = 'smartsnippets/widgets/urlfield/widget.html'


class JSONField(TextField):
    name = 'JSON Field'

    @property
    def formatted_value(self):
        try:
            return json.loads(
                self.variable.value or '{}',
                object_pairs_hook=collections.OrderedDict
            )
        except ValueError:
            pass
        return {}



widget_pool.register_widget(TextField)
widget_pool.register_widget(TextAreaField)
widget_pool.register_widget(DropDownField)
widget_pool.register_widget(SwitcherField)
widget_pool.register_widget(URLField)
widget_pool.register_widget(JSONField)
