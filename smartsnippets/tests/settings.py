import os
from django.conf import settings

shared_sites = getattr(settings, 'SMARTSNIPPETS_SHARED_SITES', [])
include_orphan = getattr(settings, 'SMARTSNIPPETS_INCLUDE_ORPHAN', True)
restrict_user = getattr(settings, 'SMARTSNIPPETS_RESTRICT_USER', False)

snippet_caching_time = getattr(settings, 'SMARTSNIPPETS_CACHING_TIME', 300)
caching_enabled = snippet_caching_time != 0

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'smartsnippets.tests.urls'
CMS_TEMPLATES = [('sample.html',) * 2 ]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cms',
    'mptt',
    'south',
    'sekizai',
    'smartsnippets',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : 'test.db', # Or path to database file if using sqlite3.
        'USER' : '', # Not used with sqlite3.
        'PASSWORD' : '', # Not used with sqlite3.
        'HOST' : '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT' : '', # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = 'c8syx=b9zy)+v$07wb+f!=&amp;#38w829lp*r$$%6i_6b@khg1-n5'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.auth.middleware.AuthenticationMiddleware'
    'django.contrib.sessions.middleware.SessionMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

HERE = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIRS = (
    os.path.join(HERE, 'templates',)
)
