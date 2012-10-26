from django.core.cache import cache
from django.db import models
from django.db.models import signals
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError, \
    TemplateDoesNotExist, loader
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from .settings import snippet_caching_time, caching_enabled


class SmartSnippet(models.Model):
    name = models.CharField(unique=True, max_length=255)
    template_code = models.TextField(_("Template code"), blank=True)
    template_path = models.CharField(
        _("Template path"),
        max_length=100, blank=True, \
        help_text=_(
                'Enter a template (i.e. "snippets/plugin_xy.html")'
                ' which will be rendered.'))
    sites = models.ManyToManyField(Site, null=False, blank=True,
        help_text=_('Select on which sites the snippet will be available.'),
        verbose_name='sites')

    class Meta:
        ordering = ['name']
        verbose_name = 'Smart Snippet'
        verbose_name_plural = 'Smart Snippets'

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

    def render(self, context, cache_snippet=False):
        return self.get_template().render(context)

    def __unicode__(self):
        return self.name


class SmartSnippetVariable(models.Model):
    name = models.CharField(
        max_length=50,
        help_text=_('Enter the name of the variable defined in '
                    'the smart snippet template.'))
    widget = models.CharField(max_length=50,
            help_text=_('Select the type of the variable defined '
                        'in the smart snippet template.'))
    snippet = models.ForeignKey(SmartSnippet, related_name="variables")

    class Meta:
        unique_together = (('snippet', 'name'))
        ordering = ['name']
        verbose_name = "Standard variable"

    def save(self, *args, **kwargs):
        super(SmartSnippetVariable, self).save(*args, **kwargs)
        smartsnippet_pointers = self.snippet.smartsnippetpointer_set.all()
        for spointer in smartsnippet_pointers:
            v, _ = Variable.objects.get_or_create(snippet=spointer, snippet_variable=self)
            v.save()

    def __unicode__(self):
        return self.name


class SmartSnippetPointer(CMSPlugin):
    snippet = models.ForeignKey(SmartSnippet)

    def get_cache_key(self):
        return 'smartsnippet-pointer-%s' % self.pk

    def render(self, context):
        cache_key = self.get_cache_key()
        if caching_enabled and cache.has_key(cache_key):
            return cache.get(cache_key)
        vars = dict((var.snippet_variable.name, var.formatted_value) for var in self.variables.all())
        context.update(vars)
        rendered_snippet = self.snippet.render(context)
        if caching_enabled:
            cache.set(cache_key, rendered_snippet, snippet_caching_time)
            # also cache a 'marker' which states that at least one pointer (self)
            # of a smart snippet type (self.snippet) has been cached
            # this is usefull for speeding up the cache invalidation
            # by not running the same query for each SmartSnippetVariable
            # that changed
            cache.set(self.snippet.get_cache_key(), '1')
        return rendered_snippet

    def __unicode__(self):
        return unicode(self.snippet)


class Variable(models.Model):
    snippet_variable = models.ForeignKey(SmartSnippetVariable, related_name='variables')
    value = models.CharField(max_length=1024)
    snippet = models.ForeignKey(SmartSnippetPointer, related_name='variables')

    class Meta:
        unique_together = (('snippet_variable', 'snippet'))

    @property
    def formatted_value(self):
        from widgets_pool import widget_pool
        widget_instance = widget_pool.get_widget(self.snippet_variable.widget)(self)
        return widget_instance.formatted_value

    @property
    def name(self):
        return self.snippet_variable.name

    @property
    def widget(self):
        return self.snippet_variable.widget


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

if caching_enabled:

    def clear_all_pointers(snippet):
        if cache.has_key(snippet.get_cache_key()):
            for snippet_pointer in snippet.smartsnippetpointer_set.all():
                cache.delete(snippet_pointer.get_cache_key())
            cache.delete(snippet.get_cache_key())

    def clear_cache_on_snippet_change(instance, **kwargs):
        clear_all_pointers(instance)

    def clear_cache_on_snippet_pointer_change(instance, **kwargs):
        cache.delete(instance.get_cache_key())

    def clear_cache_on_snippet_variable_change(instance, **kwargs):
        clear_all_pointers(instance.snippet)

    def clear_cache_on_variable_value_change(instance, **kwargs):
        cache.delete(instance.snippet.get_cache_key())

    signals.post_save.connect(clear_cache_on_snippet_change,
                              sender=SmartSnippet)
    signals.post_save.connect(clear_cache_on_snippet_pointer_change,
                              sender=SmartSnippetPointer)

    signals.post_save.connect(clear_cache_on_variable_value_change,
                              sender=Variable)

    def get_entire_hierarchy(_class):
        subclasses = []
        for subclass in _class.__subclasses__():
            subclasses += get_entire_hierarchy(subclass)
        return [_class] + subclasses

    for _cls in get_entire_hierarchy(SmartSnippetVariable):
        signals.post_save.connect(clear_cache_on_snippet_variable_change,
                                  sender=_cls)
