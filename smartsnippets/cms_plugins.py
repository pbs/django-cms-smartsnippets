from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import SmartSnippetPointer, Variable
from django.contrib import admin


class VariableInline(admin.TabularInline):
    model = Variable

class SmartSnippetPlugin(CMSPluginBase):
    model = SmartSnippetPointer
    name = 'Smart Snippet'
    render_template = 'smartsnippets/plugin.html'
    inlines = [VariableInline,]

    def render(self, context, instance, placeholder):
        context.update({'content': instance.render(context)})
        return context

plugin_pool.register_plugin(SmartSnippetPlugin)
