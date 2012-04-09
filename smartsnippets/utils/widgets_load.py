from cms.utils.django_load import get_module
from smartsnippets.settings import installed_widgets


def load(modname, verbose=False, failfast=False):
    for widget in installed_widgets:
        get_module(widget, modname, verbose, failfast)