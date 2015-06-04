from django.conf import settings

shared_sites = getattr(settings, 'SMARTSNIPPETS_SHARED_SITES', [])
include_orphan = getattr(settings, 'SMARTSNIPPETS_INCLUDE_ORPHAN', True)
restrict_user = getattr(settings, 'SMARTSNIPPETS_RESTRICT_USER', False)
handle_permissions_checks = getattr(settings, 'SMARTSNIPPETS_HANDLE_PERMISSIONS_CHECKS', True)

snippet_caching_time = getattr(settings, 'SMARTSNIPPETS_CACHING_TIME', 300)
caching_enabled = snippet_caching_time != 0


def _has_data_defined(widget_data):
    return (
        widget_data.get('widget', None) or
        widget_data.get('resources', None)
    )

custom_widgets_resources = {
    widget_type: widget_data
    for widget_type, widget_data in getattr(
        settings, 'SMARTSNIPPETS_PREDEFINED_WIDGETS', {}).items()
    if _has_data_defined(widget_data)
}

allow_inheritance = getattr(
    settings, 'SMARTSNIPPETS_ALLOW_INHERITANCE',
    'smartsnippets_inherit' in settings.INSTALLED_APPS)
inherit_variable_pattern = getattr(
    settings, 'SMARTSNIPPETS_INHERIT_VAR_PATTERN',
    '_snippet_inherit_{identifier}')

USE_BOOTSTRAP_ACE = getattr(
    settings, 'SMARTSNIPPETS_USE_BOOTSTRAP_ACE', False)
