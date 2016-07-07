from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^edit-smart-snippet/(?P<snippet_id>\d+)/',
        views.get_snippet_edit_code,
        name="smartsnippet_edit"),
)
