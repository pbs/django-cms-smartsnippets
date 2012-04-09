class SmartSnippetWidgetBase(object):
    def __init__(self):
        self.smartsnippet_instance = None
    
    def render(self, context):
        raise NotImplementedError("render needs to be implemented")