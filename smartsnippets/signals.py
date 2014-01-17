#encoding utf-8

from django.dispatch import Signal

# signal sent after a smartsnippet variable (Variable) is persisted
ss_plugin_var_saved = Signal(providing_args=["sender", "request"])
