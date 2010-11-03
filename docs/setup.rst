============
Installation
============

This section describes how to install the mothertongue application in your Django
project.


Prerequisites
-------------

The mothertongue application requires Django_ 1.1.1 or higher and django-localeurl_ 1.4 or higher.

.. _Django: http://www.djangoproject.com/download/
.. _django-localeurl: http://pypi.python.org/pypi/django-localeurl/1.4


Setup
-----

Setup consists of installing the django-localeurl middleware, the mothertongue context processor and adding ``'localeurl'`` and ``'mothertongue'``
to the installed applications list.

#. Add ``'mothertongue.context_processors.router'`` to
   ``settings.TEMPLATE_CONTEXT_PROCESSORS``::
   
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...,
        "mothertongue.context_processors.router",
    )

#. Add ``'localeurl.middleware.LocaleURLMiddleware'`` to
   ``settings.MIDDLEWARE_CLASSES``. It must come *before*
   ``'django.middleware.common.CommonMiddleware'`` or ``settings.APPEND_SLASH``
   will not work.

#. Add ``'localeurl'`` and ``'mothertongue'`` to ``settings.INSTALLED_APPS``. Because localeurl
   needs to replace the standard ``urlresolvers.reverse`` function, it is
   important to place it at the top of the list like this::

     INSTALLED_APPS = (
         'localeurl',
         'mothertongue',
         ...
     )

#. Make sure ``settings.LANGUAGE_CODE`` or its root language is in
   ``settings.LANGUAGES``. For example, if ``LANGUAGE_CODE == 'en'`` then
   ``LANGUAGES`` must contain ``'en'``.


.. _configuration:

Configuration
-------------

The application can be configured by editing the project's ``settings.py``
file. This documentation only covers settings and configuration properties specific to mothertongue.
For settings relating to `django-localeurl` please see the relevant package documentation_

.. _documentation: http://packages.python.org/django-localeurl/


Example settings.py properties::
    
    ugettext = lambda s: s
    
    USE_I18N = True
    
    TIME_ZONE = 'Europe/London'
    
    LANGUAGE_CODE = 'en'
    
    LANGUAGES = (
        ('en', ugettext('English')),
        ('es', ugettext('Spanish')),
        ('fr', ugettext('French')),
    )

    PREFIX_DEFAULT_LOCALE = False
    LOCALEURL_USE_ACCEPT_LANGUAGE = True
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",
        "mothertongue.context_processors.router",
    )
    
    MIDDLEWARE_CLASSES = (
        'localeurl.middleware.LocaleURLMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )
        
    INSTALLED_APPS = (
        'localeurl',
        'mothertongue',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.admin',
    )