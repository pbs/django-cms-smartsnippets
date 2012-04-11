from django.template.loader import render_to_string
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase


class DropDownField(SmartSnippetWidgetBase):
    name = 'DropDown Field'

    def __init__(self, label, value, **kwargs):
        super(DropDownField, self).__init__(label, value, **kwargs)
        self.choices = kwargs.get('choices')

    def render(self):
        return render_to_string('smartsnippets/widgets/dropdownfield/widget.html',
                                {'field': self})

widget_pool.register_widget(DropDownField)