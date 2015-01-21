from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, QueryDict
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from smartsnippets_inherit.models import InheritPageContent, OverwriteVariable
from smartsnippets.models import SmartSnippetPointer
from cms.utils.permissions import has_plugin_permission


@csrf_protect
def variables_edit_view(request, plugin_id):
    plugin = get_object_or_404(InheritPageContent, id=plugin_id)

    if not has_plugin_permission(request.user, plugin.plugin_type, "change"):
        raise PermissionDenied

    snippet_plugin_id = None
    if request.method == 'DELETE':
       snippet_plugin_id =  QueryDict(request.body).get('snippet_plugin')

    snippet_plugin_id = (snippet_plugin_id or
                         request.REQUEST.get('snippet_plugin'))
    if snippet_plugin_id is None:
        return HttpResponseBadRequest('Snippet plugin missing')

    snippet_plugin = get_object_or_404(
        SmartSnippetPointer, id=snippet_plugin_id
    )
    variables = snippet_plugin.variables.all()
    overwrite_variables = None

    if request.method == 'POST':
        variables = variables.select_related('snippet_variable')
        overwrite_variables = []
        for var in variables:
            new_value = request.POST.get("_%s_" % var.snippet_variable.name)
            if new_value is None:
                continue
            try:
                existing_var = OverwriteVariable.objects.get(
                    plugin=plugin, variable=var)
                existing_var.value = new_value
                existing_var.save()
                overwrite_variables.append(existing_var)
            except (OverwriteVariable.DoesNotExist, ):
                new_var = OverwriteVariable.objects.create(
                    plugin=plugin, variable=var, value=new_value)
                overwrite_variables.append(new_var)

    if overwrite_variables is None:
        overwrite_variables = OverwriteVariable.objects.filter(
            plugin=plugin, variable__in=list(variables))

    if request.method == 'DELETE':
        overwrite_variables.delete()
        overwrite_variables = []

    # transform all into Variable instances
    overwrite_as_vars = [v.to_variable() for v in overwrite_variables]
    vars_to_render = {
        var.snippet_variable.name: var
        for var in list(variables) + overwrite_as_vars
    }

    return render_to_response('smartsnippets/variables_widgets.html', {
        'plugin': plugin,
        'variables': sorted(vars_to_render.values(),
                            key=lambda var: var.snippet_variable.name)
    }, context_instance=RequestContext(request))
