from models import SmartSnippetVariable

class SmartSnippetWidgetBase(object):
    name = 'Base Widget'
    model = SmartSnippetVariable
    
    def __init__(self, variable, **kwargs):
        self.variable = variable
    
    def render(self, context):
        raise NotImplementedError("render needs to be implemented")