from django.conf import settings

shared_sites = getattr(settings, 'SMARTSNIPPETS_SHARED_SITES', [])
include_orphan = getattr(settings, 'SMARTSNIPPETS_INCLUDE_ORPHAN', True)
restrict_user = getattr(settings, 'SMARTSNIPPETS_RESTRICT_USER', False)

