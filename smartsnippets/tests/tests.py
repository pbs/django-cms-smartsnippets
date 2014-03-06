from django.contrib.sites.models import Site
from django.template import RequestContext
from django.core.cache import cache
from django import http
from django.test import TestCase
from sekizai.helpers import get_varname as sekizai_key


from smartsnippets.models import (
    SmartSnippet,
    SmartSnippetPointer,
)


def do_make_smartsnippet(template_code):
    snippet = SmartSnippet.objects.create(
        name='test_snippet',
        template_code=template_code,
    )
    example_dot_com = Site.objects.get(pk=1, domain='example.com')
    snippet.sites.add(example_dot_com)
    return snippet


def do_make_pointer(snippet):
    pointer = SmartSnippetPointer.objects.create(snippet=snippet)
    return pointer


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
    text = 'There is no spoon'
    start = '{% addtoblock "css" %}'
    end = '{% endaddtoblock %}'
    template_code = ''.join([header, text, start, css_content, end])

    def setUp(self):
        self.snippet = do_make_smartsnippet(self.template_code)
        self.snippet_pointer = do_make_pointer(self.snippet)

    def test_sekizai_context_alteration(self):
        context = make_context()
        self.assertEqual(sekizai_context(context), {})
        content = self.snippet_pointer.render(context)
        self.assertEqual(content, self.text)
        css_block = sekizai_context(context)['css']
        self.assertEqual(css_block, [self.css_content])

    def test_caching(self):
        self.snippet_pointer.render(make_context())
        cache_key = self.snippet_pointer.get_cache_key()
        cache_value = cache.get(cache_key)
        self.assertEqual(cache_value['content'], self.text)
        self.assertEqual(cache_value['sekizai']['css'], [self.css_content])

    def test_sekizai_restore(self):
        self.snippet_pointer.render(make_context())
        context = make_context()
        content = self.snippet_pointer.render(context)
        self.assertEqual(content, self.text)
        css_block = sekizai_context(context)['css']
        self.assertEqual(css_block, [self.css_content])

    def tearDown(self):
        cache.clear()
