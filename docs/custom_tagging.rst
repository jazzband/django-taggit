Customizing taggit
==================

Using a Custom Tag or Through Model
-----------------------------------
By default ``django-taggit`` uses a "through model" with a
``GenericForeignKey`` on it, that has another ``ForeignKey`` to an included
``Tag`` model.  However, there are some cases where this isn't desirable, for
example if you want the speed and referential guarantees of a real
``ForeignKey``, if you have a model with a non-integer primary key, or if you
want to store additional data about a tag, such as whether it is official.  In
these cases ``django-taggit`` makes it easy to substitute your own through
model, or ``Tag`` model.

Note: Including 'taggit' in ``settings.py`` INSTALLED_APPS list will create the 
default ``django-taggit`` and "through model" models. If you would like to use 
your own models, you will need to remove 'taggit' from ``settings.py``'s 
INSTALLED_APPS list.

To change the behavior there are a number of classes you can subclass to obtain
different behavior:

=============================== =======================================================================
Class name                      Behavior
=============================== =======================================================================
``TaggedItemBase``              Allows custom ``ForeignKeys`` to models.
``GenericTaggedItemBase``       Allows custom ``Tag`` models. Tagged models use an integer primary key.
``GenericUUIDTaggedItemBase``   Allows custom ``Tag`` models. Tagged models use a UUID primary key.
``CommonGenericTaggedItemBase`` Allows custom ``Tag`` models and ``GenericForeignKeys`` to models.
``ItemBase``                    Allows custom ``Tag`` models and ``ForeignKeys`` to models.
=============================== =======================================================================

Custom ForeignKeys
~~~~~~~~~~~~~~~~~~

Your intermediary model must be a subclass of
``taggit.models.TaggedItemBase`` with a foreign key to your content
model named ``content_object``. Pass this intermediary model as the
``through`` argument to ``TaggableManager``::

    from django.db import models

    from taggit.managers import TaggableManager
    from taggit.models import TaggedItemBase


    class TaggedFood(TaggedItemBase):
        content_object = models.ForeignKey('Food', on_delete=models.CASCADE)

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedFood)


Once this is done, the API works the same as for GFK-tagged models.

Custom GenericForeignKeys
~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``GenericForeignKey`` used by ``django-taggit`` assume your
tagged object use an integer primary key. For non-integer primary key,
your intermediary model must be a subclass of ``taggit.models.CommonGenericTaggedItemBase``
with a field named ``"object_id"`` of the type of your primary key.

For example, if your primary key is a string::

    from django.db import models

    from taggit.managers import TaggableManager
    from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

    class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
        object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)

    class Food(models.Model):
        food_id = models.CharField(primary_key=True)
        # ... fields here

        tags = TaggableManager(through=GenericStringTaggedItem)

GenericUUIDTaggedItemBase
~~~~~~~~~~~~~~~~~~~~~~~~~

A common use case of a non-integer primary key, is UUID primary key.
``django-taggit`` provides a base class ``GenericUUIDTaggedItemBase`` ready
to use with models using an UUID primary key::

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    from taggit.managers import TaggableManager
    from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

    class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
        # If you only inherit GenericUUIDTaggedItemBase, you need to define
        # a tag field. e.g.
        # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

        class Meta:
            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

    class Food(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        # ... fields here

        tags = TaggableManager(through=UUIDTaggedItem)

Custom tag
~~~~~~~~~~

When providing a custom ``Tag`` model it should be a ``ForeignKey`` to your tag
model named ``"tag"``. If your custom ``Tag`` model has extra parameters you want to initialize during setup, you can do so by passing it along via the ``tag_kwargs`` parameter of ``TaggableManager.add``. For example ``my_food.tags.add("tag_name1", "tag_name2", tag_kwargs={"my_field":3})``:

  .. code-block:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    from taggit.managers import TaggableManager
    from taggit.models import TagBase, GenericTaggedItemBase


    class MyCustomTag(TagBase):
        # ... fields here

        class Meta:
            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

        # ... methods (if any) here


    class TaggedWhatever(GenericTaggedItemBase):
        # TaggedWhatever can also extend TaggedItemBase or a combination of
        # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
        # allows using the same tag for different kinds of objects, in this
        # example Food and Drink.

        # Here is where you provide your custom Tag class.
        tag = models.ForeignKey(
            MyCustomTag,
            on_delete=models.CASCADE,
            related_name="%(app_label)s_%(class)s_items",
        )


    class Food(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedWhatever)


    class Drink(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedWhatever)


.. class:: TagBase

    .. method:: slugify(tag, i=None)

        By default ``taggit`` uses :func:`django.utils.text.slugify` to
        calculate a slug for a given tag. However, if you want to implement
        your own logic you can override this method, which receives the ``tag``
        (a string), and ``i``, which is either ``None`` or an integer, which
        signifies how many times the slug for this tag has been attempted to be
        calculated, it is ``None`` on the first time, and the counting begins
        at ``1`` thereafter.


Using a custom tag string parser
--------------------------------

By default ``django-taggit`` uses ``taggit.utils._parse_tags`` which accepts a
string which may contain one or more tags and returns a list of tag names. This
parser is quite intelligent and can handle a number of edge cases; however, you
may wish to provide your own parser for various reasons (e.g. you can do some
preprocessing on the tags so that they are converted to lowercase, reject
certain tags, disallow certain characters, split only on commas rather than
commas and whitespace, etc.). To provide your own parser, write a function that
takes a tag string and returns a list of tag names. For example, a simple
function to split on comma and convert to lowercase::

    def comma_splitter(tag_string):
        return [t.strip().lower() for t in tag_string.split(',') if t.strip()]

You need to tell ``taggit`` to use this function instead of the default by
adding a new setting, ``TAGGIT_TAGS_FROM_STRING`` and providing it with the
dotted path to your function. Likewise, you can provide a function to convert a
list of tags to a string representation and use the setting
``TAGGIT_STRING_FROM_TAGS`` to override the default value (which is
``taggit.utils._edit_string_for_tags``)::

    def comma_joiner(tags):
        return ', '.join(t.name for t in tags)

If the functions above were defined in a module, ``appname.utils``, then your
project settings.py file should contain the following::

    TAGGIT_TAGS_FROM_STRING = 'appname.utils.comma_splitter'
    TAGGIT_STRING_FROM_TAGS = 'appname.utils.comma_joiner'
