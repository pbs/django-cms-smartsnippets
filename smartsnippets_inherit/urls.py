from django.conf.urls import patterns, url, include

_snippet_inherit_urls = patterns('smartsnippets_inherit.views',
    url(r'^(?P<plugin_id>\d+)/variables_edit/$', 'variables_edit_view', name='variables_edit_tool'),
)

urlpatterns = patterns('',
    url(r'^admin/smartsnippets_inherit/', include(_snippet_inherit_urls)),
)
