from django.contrib.sites.models import Site
from django.template import RequestContext
from django.core.cache import cache
from django import http
from django.test import TestCase
from sekizai.helpers import get_varname as sekizai_key


from smartsnippets.models import (
    SmartSnippet,
    SmartSnippetVariable,
    SmartSnippetPointer,
    Variable,
)


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
        self.assertEqual(sekizai_context(context), {})
        content = self.snippet_pointer.render(context)
        css_block = sekizai_context(context)['css']
        self.assertEqual(content, self.text + self.value1)
        self.assertEqual(css_block, [self.css_content])

    def test_caching(self):
        self.snippet_pointer.render(make_context())
        cache_key = self.snippet_pointer.get_cache_key()
        cache_value = cache.get(cache_key)
        self.assertEqual(cache_value['sekizai']['css'], [self.css_content])
        self.assertEqual(cache_value['content'], self.text + self.value1)

    def test_sekizai_restore(self):
        self.snippet_pointer.render(make_context())
        context = make_context()
        content = self.snippet_pointer.render(context)
        css_block = sekizai_context(context)['css']
        self.assertEqual(css_block, [self.css_content])
        self.assertEqual(content, self.text + self.value1)

    def test_variable_cache_invalidation(self):
        self.snippet_pointer.render(make_context())
        self.variable.value = self.value2
        self.variable.save()
        context = make_context()
        content = self.snippet_pointer.render(context)
        css_block = sekizai_context(context)['css']
        self.assertEqual(css_block, [self.css_content])
        self.assertEqual(content, self.text + self.value2)

    def test_content_cache_invalidation(self):
        extra = ' extra_text'
        self.snippet_pointer.render(make_context())
        self.snippet.template_code += extra
        self.snippet.save()
        context = make_context()
        content = self.snippet_pointer.render(context)
        css_block = sekizai_context(context)['css']
        self.assertEqual(css_block, [self.css_content])
        self.assertEqual(content, self.text + self.value1 + extra)

    def tearDown(self):
        cache.clear()
