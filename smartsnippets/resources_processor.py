from collections import defaultdict
from django.contrib.admin.templatetags.admin_static import static
from django.conf import settings
import os


def get_filer_url(link):
    if 'filertags' in settings.INSTALLED_APPS:
        from filertags.templatetags.filertags import filerfile
        return filerfile(link)
    return link


def get_static_url(link):
    return static(link)


PROCESSORS = {
    'static': get_static_url,
    'filer': get_filer_url,
}


def _process(resource):
    # split processor name from resource link
    link = resource.strip().split(':', 1)

    processor_type = link[0].strip()
    if processor_type in PROCESSORS:
        processor_type, link = link
    else:
        processor_type = None
        link = link[0]

    res_type = os.path.splitext(link)[1].strip('.')
    if not res_type:
        return None

    if not processor_type:
        return (res_type, link)

    return (res_type, PROCESSORS[processor_type](link))


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
    resources = defaultdict(list)
    for resource in resources_data.split(','):
        processed_link = _process(resource)
        if not processed_link:
            continue
        links = resources[processed_link[0]]
        res_link = processed_link[1]
        # check if already added. Note: using list and not set just to
        #   make sure the ordering is kept
        if res_link not in links:
            links.append(processed_link[1])
    return resources

