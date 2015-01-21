from models import SmartSnippetVariable
from django.template.loader import render_to_string
from django.template import RequestContext


class SmartSnippetWidgetBase(object):
    name = 'Base Widget'
    model = SmartSnippetVariable
    template = None

    def __init__(self, variable, **kwargs):
        self.variable = variable

    @property
    def formatted_value(self):
        return self.variable.value

    def get_extra_data(self, request):
        return {}

    def render(self, request, context=None):
        if self.template is None:
            raise NotImplementedError(
                "render needs to be implemented or set a default template")

        default_data = {'field': self.variable}
        select_template = list(self.variable.templates) + [self.template]
        return render_to_string(
            select_template,
            dict(self.get_extra_data(request).items() + default_data.items()),
            context_instance=(context or RequestContext(request))
        )
