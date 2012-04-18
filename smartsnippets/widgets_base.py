from models import SmartSnippetVariable

class SmartSnippetWidgetBase(object):
    name = 'Base Widget'
    model = SmartSnippetVariable
    
    def __init__(self, variable, **kwargs):
        self.variable = variable
    
    def format_value(self, value):
        return value
    
    def render(self, context):
        raise NotImplementedError("render needs to be implemented")