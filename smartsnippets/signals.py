#encoding utf-8

from django.dispatch import Signal

# signal sent after a smartsnippet variable is persisted
smartsnippet_var_saved = Signal(providing_args=["sender", "request"])
