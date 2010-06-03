Getting Started
===============

To get started using ``django-taggit`` simply install it with
``pip``::

    $ pip install django-taggit


Add ``"taggit"`` to your project's ``INSTALLED_APPS`` setting.

And then to any model you want tagging on do the following::

    from django.db import models

    from taggit.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()

