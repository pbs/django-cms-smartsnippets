from django.conf import settings

shared_sites = getattr(settings, 'SMARTSNIPPETS_SHARED_SITES', [])
include_orphan = getattr(settings, 'SMARTSNIPPETS_INCLUDE_ORPHAN', True)
restrict_user = getattr(settings, 'SMARTSNIPPETS_RESTRICT_USER', False)
handle_permissions_checks = getattr(settings, 'SMARTSNIPPETS_HANDLE_PERMISSIONS_CHECKS', True)

snippet_caching_time = getattr(settings, 'SMARTSNIPPETS_CACHING_TIME', 300)
caching_enabled = snippet_caching_time != 0
custom_widgets_resources = getattr(settings, 'SMARTSNIPPETS_PREDEFINED_WIDGETS', {})
