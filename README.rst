django-taggit
=============
.. image:: https://travis-ci.org/alex/django-taggit.svg?branch=master
    :target: https://travis-ci.org/alex/django-taggit
.. image:: https://codecov.io/gh/alex/django-taggit/coverage.svg?branch=master
    :target: https://codecov.io/gh/alex/django-taggit?branch=master

``django-taggit`` a simpler approach to tagging with Django.  Add ``"taggit"`` to your
``INSTALLED_APPS`` then just add a TaggableManager to your model and go:

.. code:: python

    from django.db import models

    from taggit.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


Then you can use the API like so:

.. code:: python

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

``django-taggit`` requires Django 1.4.5 or greater.

For more info check out the `documentation <https://django-taggit.readthedocs.org/en/latest/>`_.  And for questions about usage or
development you can contact the
`mailinglist <http://groups.google.com/group/django-taggit>`_.
