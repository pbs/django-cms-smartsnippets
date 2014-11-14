from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from smartsnippets_inherit.models import InheritPageContent
from smartsnippets.models import SmartSnippetPointer
from smartsnippets.widgets_pool import widget_pool
from django.template import RequestContext


@csrf_protect
def variables_edit_view(request, plugin_id):
    plugin = get_object_or_404(InheritPageContent, id=plugin_id)

    snippet_plugin_id = request.REQUEST.get('snippet_plugin')
    if not snippet_plugin_id:
        return HttpResponseBadRequest('Snippet plugin missing')

    snippet_plugin = get_object_or_404(
        SmartSnippetPointer, id=snippet_plugin_id)


    return render_to_response('smartsnippets/variables_widgets.html', {
        'variables': [
            widget_pool.get_widget(var.widget)(var)
            for var in snippet_plugin.variables.all()]
    }, context_instance=RequestContext(request))
