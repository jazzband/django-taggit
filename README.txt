django-taggit
=============

``django-taggit`` a simpler approach to tagging with Django.  Add it to your
``INSTALLED_APPS`` then just add a TaggableManager to your model and go::

    from django.db import models

    from taggit.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


Then you can use the API like so::

    >>> apple = Food.objects.create(name="apple")
    >>> apple.tags.add("red", "green", "delicious")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: green>, <Tag: delicious>]
    >>> apple.tags.remove("green")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: delicious>]
    >>> Food.objects.filter(tags__in=["red"])
    [<Food: apple>, <Food: cherry>]

Tags will show up for you automatically in forms and the admin.

If you don't like the inefficiency of generic foreign keys, and you
know in advance which models in your project will be tagged,
django-taggit also supports tagging with direct foreign keys. You must
create your own intermediary model, a subclass of
``taggit.models.TaggedItemBase`` with a foreign key to your content
model named ``content_object``, and then pass this intermediary model
as the ``through`` argument of ``TaggableManager``::

    from django.db import models

    from taggit.managers import TaggableManager
    from taggit.models import TaggedItemBase
    
    class TaggedFood(TaggedItemBase):
        content_object = models.ForeignKey('Food')
    
    class Food(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedFood)

Once this is done, the API works identically with direct-tagged or
GFK-tagged models.

``django-taggit`` requires Django 1.1 or greater.
