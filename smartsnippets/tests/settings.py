import os

SMARTSNIPPETS_SHARED_SITES = []
SMARTSNIPPETS_INCLUDE_ORPHAN = True
SMARTSNIPPETS_RESTRICT_USER = False
SMARTSNIPPETS_CACHING_TIME = 300

DEBUG = True

ROOT_URLCONF = 'smartsnippets.tests.urls'
CMS_TEMPLATES = [('sample.html',) * 2]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cms',
    'mptt',
    'sekizai',
    'smartsnippets',
    'smartsnippets_inherit',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = 'c8syx=b9zy)+v$07wb+f!=&amp;#38w829lp*r$$%6i_6b@khg1-n5'
MIDDLEWARE_CLASSES = (
    'django.contrib.auth.middleware.AuthenticationMiddleware'
    'django.contrib.sessions.middleware.SessionMiddleware',
)

HERE = os.path.dirname(os.path.realpath(__file__))

SECRET_KEY = 'secret'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(HERE, 'templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'cms.context_processors.media',
                'sekizai.context_processors.sekizai',
            ),
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ),
            'debug': DEBUG
        },
    },
]
