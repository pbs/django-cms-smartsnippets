from django.template.loader import render_to_string
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from models import DropDownVariable

class TextField(SmartSnippetWidgetBase):
    name = 'Text Field'
    
    def render(self):
        return render_to_string('smartsnippets/widgets/textfield/widget.html',
                                    {'field': self.variable})


class TextAreaField(SmartSnippetWidgetBase):
    name = 'TextArea Field'
    
    def render(self):
        return render_to_string('smartsnippets/widgets/textareafield/widget.html',
                                    {'field': self.variable})


class DropDownField(SmartSnippetWidgetBase):
    name = 'DropDown Field'
    model = DropDownVariable
    
    def render(self):
        return render_to_string('smartsnippets/widgets/dropdownfield/widget.html',
                                {'field': self.variable})

widget_pool.register_widget(TextField)
widget_pool.register_widget(TextAreaField)
widget_pool.register_widget(DropDownField)