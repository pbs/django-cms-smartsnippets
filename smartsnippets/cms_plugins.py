from django.db.models import Q
from django.contrib.sites.models import Site

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from smartsnippets.widgets_pool import widget_pool

from .models import SmartSnippetPointer, SmartSnippet, Variable
from .settings import shared_sites, include_orphan, restrict_user


class SmartSnippetPlugin(CMSPluginBase):
    shared_sites = shared_sites
    include_orphan = include_orphan
    restrict_user = restrict_user

    change_form_template = 'smartsnippets/snippet_change_form.html'

    model = SmartSnippetPointer
    name = 'Smart Snippet'
    render_template = 'smartsnippets/plugin.html'


    def change_view(self, request, object_id, extra_context=None):
        if extra_context is None:
            extra_context = {}
        pointer = SmartSnippetPointer.objects.get(pk=object_id)
        snippet_vars = pointer.snippet.variables.all()
        variables = pointer.variables.filter(snippet_variable__in=snippet_vars).order_by('snippet_variable__name')
        extra_context.update({'variables':
            [widget_pool.get_widget(var.widget)(var) for var in variables]
        })
        return (super(SmartSnippetPlugin, self)
            .change_view(request, object_id, extra_context))

    def render(self, context, instance, placeholder):
        context.update({'content': instance.render(context)})
        return context

    def save_model(self, request, obj, form, change):
        super(SmartSnippetPlugin, self).save_model(request, obj, form, change)
        vars = obj.snippet.variables.all()
        for var in vars:
            v, _ = Variable.objects.get_or_create(snippet=obj, snippet_variable=var)
            v.value = request.REQUEST.get('_'+var.name+'_', '')
            v.save()


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "snippet":
            f = Q(sites=Site.objects.get_current())
            if self.shared_sites:
                f |= Q(sites__name__in=self.shared_sites)
            if include_orphan:
                f |= Q(sites__isnull=True)
            kwargs["queryset"] = SmartSnippet.objects.filter(f).distinct()
        return (super(SmartSnippetPlugin, self)
                    .formfield_for_foreignkey(db_field, request, **kwargs))


plugin_pool.register_plugin(SmartSnippetPlugin)
