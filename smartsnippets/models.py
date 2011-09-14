from django.db import models
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError, VariableNode
from cms.models import CMSPlugin


class SmartSnippet(models.Model):
    name = models.CharField(unique=True, max_length=255)
    template_code = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Smart Snippet'
        verbose_name_plural = 'Smart Snippets'

    def get_template(self):
        return Template(self.template_code)

    def get_variables_list(self):
        t = self.get_template()
        variable_nodes = t.nodelist.get_nodes_by_type(VariableNode)
        return [node.filter_expression.token for node in variable_nodes]

    def clean_template_code(self):
        try:
            self.get_template()
        except TemplateSyntaxError, e:
            raise ValidationError(str(e))

    def render(self, context):
        return self.get_template().render(context)

    def __unicode__(self):
        return self.name


class SmartSnippetPointer(CMSPlugin):
    snippet = models.ForeignKey(SmartSnippet)

    def render(self, context):
        vars = dict((v.name, v.value) for v in self.variables.all())
        context.update(vars)
        return self.snippet.render(context)

    def __unicode__(self):
        return unicode(self.snippet)


class Variable(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    snippet = models.ForeignKey(SmartSnippetPointer, related_name='variables')

    class Meta:
        unique_together = (('name', 'snippet'))

