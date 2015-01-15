from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.plugins.utils import downcast_plugins
from cms.models.placeholdermodel import Placeholder
from cms.models.pluginmodel import CMSPlugin
from smartsnippets_inherit.models import InheritPageContent
from smartsnippets_inherit.forms import InheritPageForm
from smartsnippets.settings import inherit_variable_pattern
from smartsnippets.models import Variable, SmartSnippetPointer
from contextlib import contextmanager
from itertools import chain


@contextmanager
def current_page(request, page):
    original_page = getattr(request, 'current_page', None)
    try:
        setattr(request, 'current_page', page)
        yield
    finally:
        setattr(request, 'current_page', original_page)


class PageInheritPlugin(CMSPluginBase):
    model = InheritPageContent
    name = "Inherit Content from Page"
    render_template = 'smartsnippets/plugin.html'
    change_form_template = 'admin/smartsnippets_inherit/plugininherit_change_form.html'
    admin_preview = False
    form = InheritPageForm
    page_only = True

    def render_inherited(self, context, instance):
        content = ''
        if not instance.from_page.published:
            return content

        inherited = instance.get_placeholder()
        if not inherited:
            return content

        # prepare variables to be passed to the context with different values
        new_vars = {}
        for overwrite_var in instance.overwrite_variables.all():
            var = overwrite_var.to_variable()
            context_var = inherit_variable_pattern.format(identifier=var.pk)
            new_vars[context_var] = var.formatted_value

        with current_page(context.get('request'), instance.from_page):
            # inject new variables in context
            #   so that snippet plugin render can pick them up
            context.update({name: value for name, value in new_vars.items()})
            # render plugins from the inherited section
            #   with the updated context
            content = inherited.render(context, None)
            # remove overwritten data from context
            for name in new_vars.keys():
                if name in context:
                    del context[name]

        return content

    def render(self, context, instance, placeholder):
        context.update({'content': self.render_inherited(context, instance)})
        return context

    def get_form(self, request, obj=None, **kwargs):
        formCls = super(PageInheritPlugin, self).get_form(
            request, obj, **kwargs)
        formCls.current_page = self.cms_plugin_instance.page or self.page
        return formCls

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        try:
            plugin = InheritPageContent.objects.get(id=object_id)
            placeholder = plugin.get_placeholder()
            extra_context.update({
                'snippet_plugins': self.get_inherited_snippets(placeholder)
            })
        except (InheritPageContent.DoesNotExist, ):
            pass
        return super(PageInheritPlugin, self).change_view(
            request, object_id, extra_context=extra_context)

    def get_inherited_snippets(self, placeholder):
        if not placeholder or not placeholder.page:
            return []

        def can_be_overwritten(plg):
            return (
                plg.__class__ is SmartSnippetPointer and
                plg.variables.exists()
            )

        page = placeholder.page
        slot = placeholder.slot
        pages = chain([page], page.get_cached_ancestors(ascending=True))
        for ancestor in pages:
            placeholder = ancestor.placeholders.filter(slot=slot)[:1]
            if not placeholder:
                continue
            placeholder = placeholder[0]
            plugins = downcast_plugins(placeholder.get_plugins())
            if not plugins:
                continue
            return sorted(
                filter(can_be_overwritten, plugins),
                key=lambda plg: plg.position,
            )
        return []


plugin_pool.register_plugin(PageInheritPlugin)
