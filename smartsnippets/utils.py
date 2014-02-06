from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils.importlib import import_module
from smartsnippets.settings import (
    colorpicker_schemes_file_location, colorpicker_schemes_file_fetcher)
from collections import OrderedDict
import json


def data_from_static_file(location):
    data = '{}'
    with open(finders.find(location), "r") as json_file:
        data = json_file.read()
    return data


class ColorPickerSchemes():

    def _get_schemes_data(self):
        raw_data = self.fetch_raw_data(colorpicker_schemes_file_location)
        json_data = json.loads(raw_data, object_pairs_hook=OrderedDict)
        self.schemes = json_data.get('schemes', [])

    def __init__(self):
        self.schemes = None

    def fetch_raw_data(self, location):
        # loads function from name and returns it
        fetch_func_name = colorpicker_schemes_file_fetcher
        module_name, object_name = fetch_func_name.rsplit('.', 1)
        return getattr(import_module(module_name), object_name)(location)

    def __iter__(self):
        if self.schemes is None:
            self._get_schemes_data()
        return iter(self.schemes)


