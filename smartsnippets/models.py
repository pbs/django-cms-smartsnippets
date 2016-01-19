import re

from django.core.cache import cache
from django.db import models
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError, \
    TemplateDoesNotExist, loader
from django.db.models import signals
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from sekizai.helpers import (
    Watcher as sekizai_context_watcher,
    get_varname as sekizai_cache_key,
)

from .resources_processor import get_resources
from .settings import (
    snippet_caching_time, caching_enabled, allow_inheritance,
    inherit_variable_pattern)


class SmartSnippet(models.Model):
    name = models.CharField(unique=True, max_length=255)
    template_code = models.TextField(_("Template code"), blank=True)
    template_path = models.CharField(
        _("Template path"),
        max_length=100, blank=True,
        help_text=_(
            'Enter a template (i.e. "snippets/plugin_xy.html")'
            ' which will be rendered.'))
    sites = models.ManyToManyField(
        Site, null=False, blank=True,
        help_text=_('Select on which sites the snippet will be available.'),
        verbose_name='sites')
    description = models.TextField(_("Description"), blank=True)
    documentation_link = models.CharField(
        _("Documentation link"),
        max_length=100, blank=True,
        help_text=_('Enter URL (i.e. "http://snippets/docs/plugin_xy.html")'
                    ' to the extended documentation.'))

    class Meta:
        ordering = ['name']
        verbose_name = 'Smart Snippet'
        verbose_name_plural = 'Smart Snippets'

    def __init__(self, *args, **kwargs):
        #hack due to
        #     https://code.djangoproject.com/ticket/16433#no1
        for rel_obj in self._meta.get_all_related_objects():
            rel_obj.help_text = ""
        super(SmartSnippet, self).__init__(*args, **kwargs)

    def get_template(self):
        if self.template_path:
            return loader.get_template(self.template_path)
        else:
            return Template(self.template_code)

    def clean_template_code(self):
        try:
            self.get_template()
        except (TemplateSyntaxError, TemplateDoesNotExist), e:
            raise ValidationError(str(e))

    def get_cache_key(self):
        return 'smartsnippet-%s' % self.pk

    def render(self, context):
        return self.get_template().render(context)

    def __unicode__(self):
        return self.name


class SmartSnippetVariable(models.Model):
    name = models.CharField(
        max_length=50,
        help_text=_('Enter the name of the variable defined in the smart snippet '
                    'template. Unallowed characters will be removed when the form is saved.'))
    widget = models.CharField(
        max_length=50,
        help_text=_('Select the type of the variable defined '
                    'in the smart snippet template.'))
    snippet = models.ForeignKey(SmartSnippet, related_name="variables")

    resources = models.TextField(_('Admin resources'), null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(SmartSnippetVariable, self).__init__(*args, **kwargs)
        self._resource_dict = None

    @property
    def resources_dict(self):
        if self._resource_dict is None:
            self._resource_dict = get_resources(self.resources)
        return self._resource_dict

    class Meta:
        unique_together = (('snippet', 'name'))
        order_with_respect_to = 'snippet'
        verbose_name = "Standard variable"

    def save(self, *args, **kwargs):
        self.name = clean_variable_name(self.name)
        super(SmartSnippetVariable, self).save(*args, **kwargs)
        # auto-generate missing variables for all snippet plugins
        plugin_ids = SmartSnippetPointer.objects \
            .filter(snippet=self.snippet) \
            .exclude(variables__snippet_variable=self) \
            .values_list('id', flat=True)
        # in order to improve performance do a bulk create
        Variable.objects.bulk_create([
            Variable(snippet_id=plugin_id, snippet_variable=self)
            for plugin_id in plugin_ids
        ])
        if not caching_enabled:
            return
        # invalidate cache for changed plugins
        cache_keys = [
            SmartSnippetPointer.cache_key_format.format(primary_key=plugin_id)
            for plugin_id in plugin_ids
        ]
        cache.delete_many(cache_keys)

    def __unicode__(self):
        return self.name


class SmartSnippetPointer(CMSPlugin):
    snippet = models.ForeignKey(SmartSnippet)
    cache_key_format = 'smartsnippet-pointer-{primary_key}'

    class Meta:
        db_table = 'cmsplugin_smartsnippetpointer'

    def get_cache_key(self):
        return self.cache_key_format.format(primary_key=self.pk)

    def _do_restore_sekizai_context(self, context, changes):
        """Sekizai tags involve magic with the context object.
        When need to restore the sekizai content to the context"""
        cache_key = sekizai_cache_key()
        sekizai_container = context.get(cache_key)
        for key, values in changes.items():
            sekizai_namespace = sekizai_container[key]
            for value in values:
                sekizai_namespace.append(value)

    def fetch_cached(self, context):
        cache_key = self.get_cache_key()
        user = context['request'].user
        if not user.is_staff and caching_enabled and cache.has_key(cache_key):
            cached_value = cache.get(cache_key)
            rendered_content = cached_value.get('content')
            sekizai = cached_value.get('sekizai')
            self._do_restore_sekizai_context(context, sekizai)
            return rendered_content

    def set_and_get_cache(self, user, sekizai_diff, content):
        if not user.is_staff and caching_enabled:
            value = {'content': content, 'sekizai': sekizai_diff}
            key = self.get_cache_key()
            cache.set(key, value, snippet_caching_time)
        return content

    def render_pointer(self, context):
        vars_qs = self.variables.select_related('snippet_variable').all()

        def var_for_context(var):
            default, overwrite = var.formatted_value, None
            if allow_inheritance:
                overwrite = context.get(
                    inherit_variable_pattern.format(identifier=var.pk))
            name = var.snippet_variable.name
            value = overwrite if overwrite is not None else default
            return (name, value)

        variables = dict(var_for_context(var) for var in vars_qs)
        context.update(variables)
        sekizai_differ = sekizai_context_watcher(context)
        content = self.snippet.render(context)
        sekizai_diff = sekizai_differ.get_changes()
        user = context.get('request').user
        return self.set_and_get_cache(user, sekizai_diff, content)

    def render(self, context):
        return self.fetch_cached(context) or self.render_pointer(context)

    def copy_relations(self, old_instance):
        for variable in old_instance.variables.all():
            variable.pk = None
            variable.snippet = self
            variable.save()

    def __unicode__(self):
        return unicode(self.snippet)


class Variable(models.Model):
    snippet_variable = models.ForeignKey(SmartSnippetVariable,
                                         related_name='variables')
    value = models.TextField()
    snippet = models.ForeignKey(SmartSnippetPointer, related_name='variables')

    class Meta:
        unique_together = (('snippet_variable', 'snippet'))

    @property
    def formatted_value(self):
        from widgets_pool import widget_pool
        widget_instance = widget_pool.get_widget(self.widget)(self)
        return widget_instance.formatted_value

    @property
    def name(self):
        return self.snippet_variable.name

    @property
    def widget(self):
        return self.snippet_variable.widget

    @property
    def templates(self):
        return self.snippet_variable.resources_dict.get('html', set())

    @property
    def js(self):
        return self.snippet_variable.resources_dict.get('js', set())

    @property
    def css(self):
        return self.snippet_variable.resources_dict.get('css', set())


class DropDownVariable(SmartSnippetVariable):
    choices = models.CharField(
        max_length=512,
        help_text=_(
            'Enter a comma separated list of choices that will be '
            'available in the dropdown variable when adding and '
            'configuring the smart snippet on a page.'))

    @property
    def choices_list(self):
        return ([choice.strip() for choice in self.choices.split(',') if choice.strip()]
                if self.choices else [])

    def save(self, *args, **kwargs):
        self.widget = 'DropDownField'
        super(DropDownVariable, self).save(*args, **kwargs)


def remove_cached_pointers(instance, **kwargs):
    if not caching_enabled:
        return

    pointer_pks = SmartSnippetPointer.objects.filter(
        snippet=instance
    ).values_list('pk', flat=True)
    cache_keys = [
        SmartSnippetPointer.cache_key_format.format(primary_key=pk)
        for pk in pointer_pks
    ]
    cache.delete_many(cache_keys)


def remove_cached_variables(instance, **kwargs):
    if not caching_enabled:
        return
    key = instance.snippet.get_cache_key()
    if key in cache:
        cache.delete(key)

def clean_variable_name(variable_name):
    """ Convert the variable name to a name that can be used as a template variable. """
    return re.sub(r"[^a-zA-Z0-9_]", '', variable_name.replace(' ', '_'))

signals.post_save.connect(remove_cached_pointers, sender=SmartSnippet)
signals.post_save.connect(remove_cached_variables, sender=Variable)
