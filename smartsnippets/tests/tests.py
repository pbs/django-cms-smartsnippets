from django.contrib import admin
from django.contrib.sites.models import Site
from django.template import RequestContext, Context, Template
from django.template.loader import render_to_string
from django.core.cache import cache
from django import http
from django.test import TestCase
from sekizai.helpers import get_varname as sekizai_key


from smartsnippets.models import (
    SmartSnippet,
    SmartSnippetVariable,
    SmartSnippetPointer,
    Variable,
    UnrenderableSmarSnippet,
)
from smartsnippets.templatetags.smartsnippets_tags import render_rendering_error



class FakeSiteAdmin(admin.ModelAdmin):
    """ smartsnippets.admin module requires a model admin to be registed for Site, so fake it. """
    pass
admin.site.register(Site, FakeSiteAdmin)
from smartsnippets.admin import SnippetAdmin, SnippetForm


def do_make_smartsnippet(template_code):
    snippet, _ = SmartSnippet.objects.get_or_create(
        name='test_snippet',
        template_code=template_code,
    )
    example_dot_com = Site.objects.get(pk=1, domain='example.com')
    snippet.sites.add(example_dot_com)
    return snippet


def do_make_pointer(snippet):
    pointer, _ = SmartSnippetPointer.objects.get_or_create(snippet=snippet)
    return pointer


def do_make_snippet_variable_type(snippet):
    variable_type, _ = SmartSnippetVariable.objects.get_or_create(
        snippet=snippet,
        name='item',
        widget='TextField',
    )
    return variable_type


def do_make_snippet_variable(variable_type, value, snippet_pointer):
    variable, _ = Variable.objects.get_or_create(
        snippet_variable=variable_type,
        snippet=snippet_pointer
    )
    variable.value = value
    variable.save()
    return variable


class NonStaffUser(object):
    is_staff = False


def make_context():
    context, request = RequestContext({}), http.HttpRequest()
    request.user = NonStaffUser()
    context['request'] = request
    return context


def sekizai_context(context):
    key = sekizai_key()
    content = context[key]
    return content


class TestSekizaiCache(TestCase):
    css_content = '<style type="text/css">body { color: red; }</style>'
    header = '{% load sekizai_tags %}'
    text = 'There is no '
    text_variable = '{{ item }}'
    start = '{% addtoblock "css" %}'
    end = '{% endaddtoblock %}'
    template_code = ''.join([
        header, text, text_variable, start, css_content, end])
    value1 = 'spoon'
    value2 = 'try'

    def setUp(self):
        self.snippet = do_make_smartsnippet(self.template_code)
        self.snippet_pointer = do_make_pointer(self.snippet)
        self.variable_type = do_make_snippet_variable_type(self.snippet)
        self.variable = do_make_snippet_variable(
            variable_type=self.variable_type,
            value=self.value1,
            snippet_pointer=self.snippet_pointer
        )

    def test_sekizai_context_alteration(self):
        context = make_context()
        with context.bind_template(Template("")):
            self.assertEqual(sekizai_context(context), {})
            content = self.snippet_pointer.render(context)
            css_block = sekizai_context(context)['css']
            self.assertEqual(content, self.text + self.value1)
            self.assertEqual(css_block, [self.css_content])

    def test_caching(self):
        context = make_context()
        with context.bind_template(Template("")):
            self.snippet_pointer.render(context)
            cache_key = self.snippet_pointer.get_cache_key()
            cache_value = cache.get(cache_key)
            self.assertEqual(
                cache_value['sekizai']['css'], [self.css_content])
            self.assertEqual(
                cache_value['content'], self.text + self.value1)

    def test_sekizai_restore(self):
        context = make_context()
        with context.bind_template(Template("")):
            self.snippet_pointer.render(context)
            content = self.snippet_pointer.render(context)
            css_block = sekizai_context(context)['css']
            self.assertEqual(css_block, [self.css_content])
            self.assertEqual(content, self.text + self.value1)

    def test_variable_cache_invalidation(self):
        context = make_context()
        with context.bind_template(Template("")):
            self.snippet_pointer.render(context)
            self.variable.value = self.value2
            self.variable.save()
        context = make_context()
        with context.bind_template(Template("")):
            content = self.snippet_pointer.render(context)
            css_block = sekizai_context(context)['css']
            self.assertEqual(css_block, [self.css_content])
            self.assertEqual(content, self.text + self.value2)

    def test_content_cache_invalidation(self):
        context = make_context()
        with context.bind_template(Template("")):
            self.snippet_pointer.render(context)
            extra = ' extra_text'
            self.snippet.template_code += extra
            self.snippet.save()
        context = make_context()
        with context.bind_template(Template("")):
            content = self.snippet_pointer.render(context)
            css_block = sekizai_context(context)['css']
            self.assertEqual(css_block, [self.css_content])
            self.assertEqual(content, self.text + self.value1 + extra)

    def tearDown(self):
        cache.clear()


class TestVariables(TestCase):

    def setUp(self):
        self.snippet = SmartSnippet.objects.create(template_code='test')
        self.plugin1 = SmartSnippetPointer.objects.create(snippet=self.snippet)
        self.plugin2 = SmartSnippetPointer.objects.create(snippet=self.snippet)

    def test_vars_generated(self):
        self.assertEqual(Variable.objects.count(), 0)

        ssvar = SmartSnippetVariable.objects.create(
            snippet=self.snippet, name='item', widget='TextField')
        self.assertEqual(self.plugin1.variables.count(), 1)
        self.assertEqual(self.plugin2.variables.count(), 1)
        # add another plugin
        plugin3 = SmartSnippetPointer.objects.create(snippet=self.snippet)
        ssvar.save()
        self.assertEqual(Variable.objects.count(), 3)
        self.assertEqual(plugin3.variables.count(), 1)

    def test_validation_passes_for_correct_variables(self):
        valid_variable_requests=[
            'name=test&variables-0-name=correct_var_1&variables-1-name=also_correct%$^^ ',
            'name=test&variables-0-name=simple',
            'name=test&variables-0-name=standard&variables-2-0-name=dropdown'
            ]
        for valid_variable_request in valid_variable_requests:
            form = SnippetForm(http.QueryDict(valid_variable_request))
            self.assertTrue(form.is_valid(),
                            '{} request should be valid'.format(valid_variable_requests))

    def test_variable_name_is_cleaned(self):
        variable = SmartSnippetVariable.objects.create(
            snippet=self.snippet, name='item&&&& _name', widget='TextField')
        variable.save()
        self.assertEqual(variable.name, 'item__name')

    def test_validation_fails_for_same_name_variables(self):
        variables_requests = [
            ('name=test&variables-0-name=var_1&variables-2-0-name=var_1%^',
             u'The variable name "var_1" is used multiple times.'),
            ('name=test&variables-0-name=var_1&variables-2-0-name=var_1%^&'
             'variables-1-name=var2&variables-2-name=var2',
             u'The variable names "var_1, var2" are used multiple times.'),
            ('name=test&variables-0-name=var_1&variables-2-0-name=var_1%^&'
             'variables-1-name=var_1',
             u'The variable name "var_1" is used multiple times.'),
            ('name=test&variables-0-name=var_1&variables-2-0-name=var_1%^&'
             'variables-1-name=var2&variables-2-name=var2&variables-3-name=var2',
             u'The variable names "var_1, var2" are used multiple times.')
            ]
        for request, expected_error in variables_requests:
            form = SnippetForm(http.QueryDict(request))
            self.assertFalse(form.is_valid())
            self.assertDictEqual(form.errors, {'__all__': [expected_error]})


class TestTemplateTags(TestCase):

    class EasterEgg(object):

        def __init__(self, color):
            self.color = color

    def setUp(self):
        self.colors = 'red green blue'
        self.context_colors = {color: color for color in self.colors.split()}
        self.eggs = [self.EasterEgg(color) for color in self.colors.split()]

    def _render(self, code, data):
        ctx = Context(data or {})
        return Template("{% load smartsnippets_tags %}" + code).render(ctx)

    def test_map_by_attribute(self):
        out = self._render(
            "{{ eggs|map_by:'attribute,color'|join:' ' }}",
            {'eggs': self.eggs})
        self.assertEqual(out, self.colors)

    def test_map_by_key(self):
        objs = [{'image': 'img', 'color': c} for c in self.colors.split()]

        out = self._render(
            "{{ objs|map_by:'key,color'|join:' ' }}", {'objs': objs})
        self.assertEqual(out, self.colors)

    def test_from_context(self):
        out = self._render(
            "{% from_context 'colors' as out %}{{out}}",
            {'colors': self.colors})
        self.assertEqual(out, self.colors)

        out = self._render(
            "{% from_context 'red,green,blue' as out %}{{out|join:' '}}",
            self.context_colors)
        self.assertEqual(out, self.colors)
        # test missing name + empty val
        out = self._render(
            "{% from_context 'red green black' ' ' 'yellow' as out %}"
            "{{out|join:' '}}",
            self.context_colors)
        self.assertEqual(out, "red green yellow")

    def test_exclude_empty(self):
        out = self._render(
            "{{ objs|exclude_empty|join:'' }}",
            {'objs': ['', None, 'default']})
        self.assertEqual(out, 'default')

        objs = [{'attr': 'attr', 'color': c} for c in self.colors.split()]
        objs += [{'color': '',}, {'color': None,}, {}]
        out = self._render(
            "{{ objs|exclude_empty:'key,color'|map_by:'key,color'|join:'' }}",
            {'objs': objs})
        self.assertEqual(out, self.colors.replace(' ', ''))

    def test_json_rendering_no_config(self):
        incomplete_configs = [
            {},
            {'data': {}},
            {'data': {'metadata': None}},
            {'data': {'metadata': {'snippet_id': None}}},
        ]
        expected = render_rendering_error('Could not render smart snippet with UUID:None', '')
        for incomplete_config in incomplete_configs:
            out = self._render(
                "{% jsonsmartsnippet data id %}",
                incomplete_config)
            self.assertEqual(out, expected)


    def test_json_rendering_incorrect_snippet_id(self):
        for ss_id in ['incorrect', 12]:
            expected = render_rendering_error(
                'Could not render smart snippet with id:{}'.format(ss_id), '')
            out = self._render(
                "{% jsonsmartsnippet data id %}",
                {'data': {'metadata': {'snippet_id': ss_id}}})
            self.assertEqual(out, expected)

    def test_json_rendering_incorrect_snippet(self):
        ss_invalid = SmartSnippet.objects.create(template_code="{{ a|add:b }}")
        expected = render_rendering_error(
            'Could not render smart snippet with id:{}. Rendering error.'.format(
                ss_invalid.id), '')
        out = self._render(
            "{% jsonsmartsnippet data id %}",
            {'data': {'metadata': {'snippet_id': ss_invalid.id}}, 'id': 'uu-123'})
        self.assertEqual(out, expected)


class TestRendering(TestCase):

    def setUp(self):
        self.broken_snippet = do_make_smartsnippet('{{ var|add:other_var }}')
        self.pointer_to_broken_snippet = do_make_pointer(self.broken_snippet)

    def test_render_broken_pointer(self):
        context = make_context()
        actual = self.pointer_to_broken_snippet.render_pointer(context)
        expected = render_to_string("smartsnippets/unrenderable_smartsnippet.html",
                                    {'plugin_name': str(self.pointer_to_broken_snippet)})
        self.assertEqual(actual, expected)

    def test_not_render_broken_pointer(self):
        context = make_context()
        with self.assertRaises(UnrenderableSmarSnippet):
            self.pointer_to_broken_snippet.render_pointer(context, handle_errors=False)
