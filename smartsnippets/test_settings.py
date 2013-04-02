import os

DBTEMPLATES_CACHE_BACKEND = 'dummy://'

DATABASE_ENGINE = 'sqlite3'
# SQLite does not support removing unique constraints (see #28)
SOUTH_TESTS_MIGRATE = False

SITE_ID = 1


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHE_BACKEND = 'locmem:///'

SITE_ID = 1

USE_I18N = True
MEDIA_ROOT = '/media/'
STATIC_ROOT = '/static/'
CMS_MEDIA_ROOT = '/cms-media/'
CMS_MEDIA_URL = '/cms-media/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
SECRET_KEY = 'something-something'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'cms',
    'mptt',
    'south',
    'smartsnippets',
    'django_nose',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'dbtemplates.loader.Loader',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CMS_TEMPLATES = (
    ('test-template.html', 'Test Template'),
    )

CMS_MODERATOR = True

CMS_PERMISSION = True

MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'cms.middleware.multilingual.MultilingualURLMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.doc.XViewMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
        )

TEMPLATE_CONTEXT_PROCESSORS = (
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.i18n",
            "django.core.context_processors.request",
            "django.core.context_processors.debug",
            "django.core.context_processors.media",
            'django.core.context_processors.csrf',
            "cms.context_processors.media",
            "sekizai.context_processors.sekizai",
            "django.core.context_processors.static",
        )

TEMPLATE_DIRS = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'project', 'templates'))
        )

TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )
