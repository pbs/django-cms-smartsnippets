from django.conf import settings

CMSPLUGIN_INHERIT_NAME = getattr(settings, 'SMARTSNIPPETS_INHERIT_PLUGIN_NAME', '')
