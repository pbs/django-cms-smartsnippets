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
            footer_links = footer.get('links', [{}] * 4)
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


PRESET_SCHEMES = [{
        'base': '#cc0000',
        'background':'#e06666',
        'accent_1':'#660000',
        'accent_2':'#f6b26b',
        'accent_3':'#f9cb9c',
        'name' : 'Red Theme'    
    },{
        'base': '#660000',
        'background':'#ea9999',
        'accent_1':'#4c1130',
        'accent_2':'#c27ba0',
        'accent_3':'#d5a6bd',
        'name' : 'Red Theme 2'    
    },{
        'base': '#00ffff',
        'background':'#a2c4c9',
        'accent_1':'#0c343d',
        'accent_2':'#45818e',
        'accent_3':'#76a5af',
        'name' : 'Explorer Turquoise'    
    },{
        'base': '#2b78e4',
        'background':'#9fc5f8',
        'accent_1':'#085394',
        'accent_2':'#6fa8dc',
        'accent_3':'#b4a7d6',
        'name' : 'Blue'    
    }]

class ColorPickerField(SmartSnippetWidgetBase):
    name = 'Color Picker Field'

    def render(self, request):
        context_instance = RequestContext(request)

        return render_to_string(
            'smartsnippets/widgets/colorpickerfield/widget.html', {
                'field': self.variable,
                'preset_schemes' : PRESET_SCHEMES
            },
            context_instance=context_instance)

widget_pool.register_widget(TextField)
widget_pool.register_widget(TextAreaField)
widget_pool.register_widget(DropDownField)
widget_pool.register_widget(FlexibleFooterField)
widget_pool.register_widget(ColorPickerField)
