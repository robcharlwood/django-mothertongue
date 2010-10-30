Welcome to django-mothertongue
==============================

A light-weight translation application designed to simplify the process of creating multi-lingual websites and serving appropriate content.

Some reasons for using mothertongue:

    * In-built integration with `django-localeurl`_ 1.4 or above
    * Automatic langauge detection and redirect based on the user's browser settings
    * Automatic redirecting, state and querystring persistence on language change
    * Language navigation menu object made available globally for easy implementation of language changing controls
    * Extend from django-mothertongues' translation model to allow translation of any model you choose in as many languages as you define in your settings file
    * No fiddly language template tags - django-mothertongue handles all the magic!
    * Translate all your model fields or just one or two
    * django-mothertongue is compatible with django-tinymce
    * django-mothertongue can work side by side with django-rosetta or on its own
    * Search engines will index all languages.

.. _django-localeurl: http://pypi.python.org/pypi/django-localeurl/1.4


You can install mothertongue with pip

    pip install django-mothertongue

.. comment: split here

The mothertongue code is licensed under the `MIT License`_. See the
``LICENSE.txt`` file in the distribution.

.. _`MIT License`: http://www.opensource.org/licenses/mit-license.php


Documentation
-------------

.. toctree::
	:maxdepth: 2

	setup
	usage
	history
