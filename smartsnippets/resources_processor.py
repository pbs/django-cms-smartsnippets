from collections import defaultdict
from django.contrib.admin.templatetags.admin_static import static
from django.conf import settings
import os

try:
    from filertags.templatetags.filertags import filerfile
except ImportError:
    filerfile = None


def get_filer_url(link):
    return filerfile(link) if filerfile else link


def get_static_url(link):
    return static(link)


processors = {
    'static': get_static_url,
    'filer': get_filer_url,
}


def _process(resource):
    # split processor name from resource link
    link = resource.strip().split(':', 1)

    processor_type = link[0].strip()
    if processor_type in processors:
        processor_type, link = link
    else:
        processor_type = None

    res_type = os.path.splitext(link)[1].strip('.')
    if not res_type:
        return None

    if not processor_type:
        return (res_type, link)

    return (res_type, processors[processor_type](link))


def get_resources(resources_data):
    """
        Parses resources_data to get all resources defined with
    the following format:
        snippet-field/custom.html, static: admin/style.css,
            http://somesite/absolute-url.js
    and returns a dictionary with resources extensions and the links defined.
    """
    if not resources_data:
        return {}
    resources_data = resources_data or ''
    resources = defaultdict(set)
    for resource in resources_data.split(','):
        processed_link = _process(resource)
        if not processed_link:
            continue
        resources[processed_link[0]].append(processed_link[1])
    return resources

