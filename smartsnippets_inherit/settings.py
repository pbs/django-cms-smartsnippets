from django.conf import settings

USE_BOOTSTRAP_ACE = getattr(
    settings, 'SMARTSNIPPETS_INHERIT_USE_BOOTSTRAP_ACE', False)