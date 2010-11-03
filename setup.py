#!/usr/bin/env python
#
# Copyright (c) 2010 Rob Charlwood
# Licensed under the terms of the MIT License (see LICENSE.txt)

from setuptools import setup

# grab package metadata
app_name = __import__('mothertongue').get_appname()
version = __import__('mothertongue').get_version(limit=3)
copyright = __import__('mothertongue').get_copyright()
author = __import__('mothertongue').get_author()
long_description = open('docs/index.rst').read().split('split here', 1)[0] + """

See the `full documentation`_.

.. _`full documentation`: http://packages.python.org/django-mothertongue/
"""

setup(
    name = "django-%s" % app_name,
    version = version,
    packages = ['mothertongue', 'mothertongue.tests'],
    install_requires = [
        "django >= 1.1.1",
        "django-localeurl >= 1.4"
    ],
    author = author,
    author_email = "robcharlwood@gmail.com",
    maintainer = "Rob Charlwood",
    maintainer_email = "robcharlwood@gmail.com",
    description = "A light-weight translation application designed to simplify the process of creating multi-lingual websites and serving appropriate content.",
    long_description = long_description,
    license = "MIT License",
    keywords = "django i18n model translation",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
    ],
    url = "https://github.com/robcharlwood/django-mothertongue",
    test_suite = 'mothertongue.tests.runtests.runtests',
    zip_safe=False,
)
