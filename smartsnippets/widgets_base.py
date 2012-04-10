class SmartSnippetWidgetBase(object):
    
    def __init__(self, label, value, **kwargs):
        self.label = label
        self.value = value
    
    def render(self, context):
        raise NotImplementedError("render needs to be implemented")