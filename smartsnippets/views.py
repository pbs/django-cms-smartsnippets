import json

from django.contrib.admin.templatetags.admin_static import static
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.forms.widgets import Media as WidgetsMedia
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from cms.models import Page

from smartsnippets.cms_plugins import variables_media
from smartsnippets.models import SmartSnippet, SmartSnippetPointer, Variable


def get_snippet_edit_code(request, snippet_id, config=None):
    """
    Returns a HTTPResponse that renders the admin of a smartsnippet.

    :param request: Request needed to create the rendering context
    :param snippet_id: id of the smartsnippet model
    :param config: dictionary containing existing configuration of the smartsnippet instance,
                   None if new
    Schema: {
      'metadata': {
        'snippet_id': snippet_id,
      },
      'variables':{
        smart_snipet_variable_name: deserialized_variable_data,
      },
    }
    """
    snippet = get_object_or_404(SmartSnippet, id=snippet_id)
    snippet_vars = snippet.variables.all().order_by('_order', 'name')
    fake_pointer = SmartSnippetPointer(snippet=snippet)
    current_site = Site.objects.get_current()
    page = Page(site=current_site)
    variables_data = config.get('variables', {}) if config else {}

    def make_var(snippet_var):
        var = Variable(snippet=fake_pointer, snippet_variable=snippet_var)
        if snippet_var.name in variables_data:
            var.value = json.dumps(variables_data[snippet_var.name])
        return var

    variables = [make_var(snippet_var) for snippet_var in snippet_vars]
    media = _make_media_for_variables(variables)
    request.current_page = page
    context = {
        'is_popup': True,
        'is_popup_var': '_popup',
        'documentation_link': snippet.documentation_link,
        'description': snippet.description,
        'name': snippet.name,
        'plugin': fake_pointer,
        'original': fake_pointer,
        'variables': variables,
        'media': media,
        'current_site': current_site.id,
        'form_url': '',
        'has_file_field': True,
    }
    return render(request, 'smartsnippets/json_snippet_render.html', context)


def _make_media_for_variables(variables=None):
    media_obj = WidgetsMedia(
        js=((
            static('admin/js/core.js'),
            static('admin/js/admin/RelatedObjectLookups.js'),
            static('libs/jquery-2.1.1.min.js'),
            static('libs/bootstrap/js/bootstrap.min.js'),
            static('admin/js/custom.js'),
        )),
        css={
            'all': (
                '//fonts.googleapis.com/css?family=Open+Sans:400,300',
                static('libs/bootstrap/css/bootstrap.css'),
                static('libs/ace/css/ace.min.css'),
                static('admin/css/custom.css'), )
        }
    )
    media_obj.add_js((
        reverse('admin:jsi18n'),
        static('admin/js/SmartSnippetLib.js'),
        static('admin/js/jquery.init.js'),
        static('admin/js/default.jQuery.init.js'),
    ))
    variables_media(media_obj, variables)
    return media_obj
