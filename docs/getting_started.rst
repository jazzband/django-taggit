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

    If you want ``django-taggit`` to be **CASE INSENSITIVE** when looking up existing tags, you'll have to set to ``True`` the TAGGIT_CASE_INSENSITIVE setting (by default ``False``)::

      TAGGIT_CASE_INSENSITIVE = True
