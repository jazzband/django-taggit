Getting Started
===============

To get started using ``django-taggit`` simply install it with
``pip``::

    $ pip install django-taggit


Add ``"taggit"`` to your project's ``INSTALLED_APPS`` setting.

Run `./manage.py migrate`.

And then to any model you want tagging on do the following::

    from django.db import models

    from taggit.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()

.. note::

    If you want ``django-taggit`` to be **CASE-INSENSITIVE** when looking up existing tags, you'll have to set ``TAGGIT_CASE_INSENSITIVE`` (in ``settings.py`` or wherever you have your Django settings) to ``True`` (``False`` by default)::

      TAGGIT_CASE_INSENSITIVE = True


Settings
--------

The following Django-level settings affect the behavior of the library

* ``TAGGIT_CASE_INSENSITIVE``

  When set to ``True``, tag lookups will be case insensitive. This defaults to ``False``.

* ``TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING``
  When this is set to ``True``, tag slugs will be limited to ASCII characters. In this case, if you also have ``unidecode`` installed,
  then tag sluggification will transform a tag like ``あい　うえお`` to ``ai-ueo``.
  If you do not have ``unidecode`` installed, then you will usually be outright stripping unicode, meaning that something like ``helloあい`` will be slugified as ``hello``.

  This value defaults to ``False``, meaning that unicode is preserved in slugification.

  Because the behavior when ``True`` is set leads to situations where
  slugs can be entirely stripped to an empty string, we recommend not activating this.
