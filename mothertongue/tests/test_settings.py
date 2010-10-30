# test settings for mothertongue package
import os
ugettext = lambda s: s 
BASE_DIR = os.path.dirname(__file__)
INSTALLED_APPS = (
    'localeurl',
    'django.contrib.contenttypes',
    'mothertongue',
    'mothertongue.tests',
    )

DATABASE_ENGINE = 'sqlite3'
USE_I18N = True
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('fr', ugettext('French')),
)
PREFIX_DEFAULT_LOCALE = False
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "mothertongue.context_processors.router",
)
MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)