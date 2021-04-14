django-taggit
=============

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband

.. image:: https://img.shields.io/pypi/pyversions/django-taggit.svg
   :target: https://pypi.org/project/django-taggit/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/djversions/django-taggit.svg
   :target: https://pypi.org/project/django-taggit/
   :alt: Supported Django versions

.. image:: https://github.com/jazzband/django-taggit/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-taggit/actions
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/jazzband/django-taggit/coverage.svg?branch=master
    :target: https://codecov.io/gh/jazzband/django-taggit?branch=master

This is a `Jazzband <https://jazzband.co>`_ project. By contributing you agree
to abide by the `Contributor Code of Conduct
<https://jazzband.co/about/conduct>`_ and follow the `guidelines
<https://jazzband.co/about/guidelines>`_.

``django-taggit`` a simpler approach to tagging with Django.  Add ``"taggit"`` to your
``INSTALLED_APPS`` then just add a TaggableManager to your model and go:

.. code:: python

    from django.db import models

    from taggit.managers import TaggableManager


    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


Then you can use the API like so:

.. code:: pycon

    >>> apple = Food.objects.create(name="apple")
    >>> apple.tags.add("red", "green", "delicious")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: green>, <Tag: delicious>]
    >>> apple.tags.remove("green")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: delicious>]
    >>> Food.objects.filter(tags__name__in=["red"])
    [<Food: apple>, <Food: cherry>]

Tags will show up for you automatically in forms and the admin.

``django-taggit`` requires Django 1.11 or greater.

For more info check out the `documentation
<https://django-taggit.readthedocs.io/>`_. And for questions about usage or
development you can create an issue on Github (if your question is about
usage please add the `question` tag).
