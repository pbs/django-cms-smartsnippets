import json
from django.template.loader import render_to_string
from django.template import RequestContext
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from models import DropDownVariable

class TextField(SmartSnippetWidgetBase):
    name = 'Text Field'
    
    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/textfield/widget.html',
                                    {'field': self.variable},
                                    context_instance=context_instance)


class TextAreaField(SmartSnippetWidgetBase):
    name = 'TextArea Field'
    
    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/textareafield/widget.html',
                                    {'field': self.variable},
                                    context_instance=context_instance)


class DropDownField(SmartSnippetWidgetBase):
    name = 'DropDown Field'
    model = DropDownVariable
    
    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/dropdownfield/widget.html',
                                {'field': self.variable},
                                    context_instance=context_instance)
EMPTY_LINK = {
    'text': '',
    'url': ''
}

EMPTY_DETAILS = {
    'logo': '',
    'logo_link': '',
    'address': '',
    'phone': '',
    'fax': ''
}

class FlexibleFooterField(SmartSnippetWidgetBase):
    name = 'Flexible Footer Field'

    @property
    def formatted_value(self):
        json_string = self.variable.value or '""'
        try:
            footer = json.loads(json_string)
        except ValueError:
            footer = {}
        return footer

    def render(self, request):
        context_instance = RequestContext(request)
        footer = self.formatted_value or {}

        def get_default_links():
            footer_links = footer.get('links',[{}] * 4)
            for col in footer_links:
                col["header"] = col.get('header', EMPTY_LINK)
                col["column_links"] = col.get('column_links', [EMPTY_LINK] * 6)
        
            return footer_links


        footer['links'] = footer.get('links', get_default_links())
        footer['details'] = footer.get('details', EMPTY_DETAILS)
        footer['copyright'] = footer.get('copyright', '')

        return render_to_string(
            'smartsnippets/widgets/flexiblefooterfield/widget.html', {
                'field': self.variable,
                'footer': footer,
            },
            context_instance=context_instance)

widget_pool.register_widget(TextField)
widget_pool.register_widget(TextAreaField)
widget_pool.register_widget(DropDownField)
widget_pool.register_widget(FlexibleFooterField)