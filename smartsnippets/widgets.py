import json
from collections import OrderedDict
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


PRESET_SCHEMES = [OrderedDict([
        ('main_color', '#efa80e'),
        ('background', '#ffffff'),
        ('button_color', '#ef850d'),
        ('light_accent', '#0087bb'),
        ('darker_accent', '#016e97'),
        ('name', 'Yellow Theme')    
    ]),OrderedDict([
        ('main_color', '#589846'),
        ('background', '#f3f4ee'),
        ('button_color', '#ef850f'),
        ('light_accent', '#7eb750'),
        ('darker_accent', '#1f6038'),
        ('name', 'Green Theme')    
    ]),OrderedDict([
        ('main_color', '#ee4a2f'),
        ('background', '#f1f0ec'),
        ('button_color', '#9a8783'),
        ('light_accent', '#27314c'),
        ('darker_accent', '#ff3d1f'),
        ('name', 'Red Theme')    
    ]),OrderedDict([
        ('main_color', '#5d3b6d'),
        ('background', '#f8f3f0'),
        ('button_color', '#7e5a88'),
        ('light_accent', '#a69ca7'),
        ('darker_accent', '#46324b'),
        ('name', 'Purple Theme')    
    ]),OrderedDict([
        ('main_color', '#ee6225'),
        ('background', '#f8f3f0'),
        ('button_color', '#d24a10'),
        ('light_accent', '#20639a'),
        ('darker_accent', '#0b3a64'),
        ('name', 'Orange Theme')    
    ]),OrderedDict([
        ('main_color', '#c1ad94'),
        ('background', '#ffffff'),
        ('button_color', '#404955'),
        ('light_accent', '#8697a5'),
        ('darker_accent', '#687a92'),
        ('name', 'Neutral Theme')    
    ]),OrderedDict([
        ('main_color', '#ee4a2f'),
        ('background', '#f1f0ec'),
        ('button_color', '#9a8783'),
        ('light_accent', '#faa232'),
        ('darker_accent', '#27314c'),
        ('name', 'Orange/Purple Theme')    
    ])]

class ColorPickerField(SmartSnippetWidgetBase):
    name = 'Color Picker Field'

    @property
    def formatted_value(self):
        json_string = self.variable.value or '""'
        try:
            scheme = json.loads(json_string)
        except ValueError:
            scheme = {}
        return scheme

    def render(self, request):
        context_instance = RequestContext(request)
        scheme = self.formatted_value or {}

        return render_to_string(
            'smartsnippets/widgets/colorpickerfield/widget.html', {
                'field': self.variable,
                'preset_schemes' : PRESET_SCHEMES,
                'scheme': scheme
            },
            context_instance=context_instance)

class ColorField(SmartSnippetWidgetBase):
    name = 'Color Field'
    
    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/colorfield/widget.html',
                                    {'field': self.variable},
                                    context_instance=context_instance)


class FlexibleHeaderField(SmartSnippetWidgetBase):
    name = 'Flexible Header Field'

    @property
    def formatted_value(self):
        json_string = self.variable.value or '""'
        try:
            header = json.loads(json_string)
        except ValueError:
            header = {}
        return header

    def render(self, request):
        context_instance = RequestContext(request)
        header = self.formatted_value or {}

        return render_to_string(
            'smartsnippets/widgets/flexibleheaderfield/widget.html', {
                'field': self.variable,
                'header': header
            },
            context_instance=context_instance)

widget_pool.register_widget(TextField)
widget_pool.register_widget(TextAreaField)
widget_pool.register_widget(DropDownField)
widget_pool.register_widget(FlexibleFooterField)
widget_pool.register_widget(ColorPickerField)
widget_pool.register_widget(FlexibleHeaderField)
widget_pool.register_widget(ColorField)
