The API
=======

After you've got your ``TaggableManager`` added to your model you can start
playing around with the API.

.. class:: TaggableManager([verbose_name="Tags", help_text="A comma-separated list of tags.", through=None, blank=False])

    :param verbose_name: The verbose_name for this field.
    :param help_text: The help_text to be used in forms (including the admin).
    :param through: The through model, see :doc:`custom_tagging` for more
        information.
    :param blank: Controls whether this field is required.

    .. method:: add(*tags, through_defaults=None, tag_kwargs=None)

        This adds tags to an object. The tags can be either ``Tag`` instances, or
        strings::

            >>> apple.tags.all()
            []
            >>> apple.tags.add("red", "green", "fruit")

        Use the ``through_defaults`` argument to specify values for your custom
        ``through`` model, if needed.

        The ``tag_kwargs`` argument allows one to specify parameters for the tags
        themselves.

    .. method:: remove(*tags)

        Removes a tag from an object. No exception is raised if the object
        doesn't have that tag.

    .. method:: clear()

        Removes all tags from an object.

    .. method:: set(*tags, through_defaults=None, clear=False)

        If ``clear = True`` removes all the current tags and then adds the
        specified tags to the object. Otherwise sets the object's tags to those
        specified, removing only the missing tags and adding only the new tags.

        Use the ``through_defaults`` argument to specify values for your custom
        ``through`` model, if needed.

    .. method: most_common()

        Returns a ``QuerySet`` of all tags, annotated with the number of times
        they appear, available as the ``num_times`` attribute on each tag. The
        ``QuerySet``is ordered by ``num_times``, descending.  The ``QuerySet``
        is lazily evaluated, and can be sliced efficiently.

        :param min_count: Specify a min count to limit the returned queryset

    .. method:: similar_objects()

        Returns a list (not a lazy ``QuerySet``) of other objects tagged
        similarly to this one, ordered with most similar first. Each object in
        the list is decorated with a ``similar_tags`` attribute, the number of
        tags it shares with this object.

        If the model is using generic tagging (the default), this method
        searches tagged objects from all classes. If you are querying on a
        model with its own tagging through table, only other instances of the
        same model will be returned.

    .. method:: names()

        Convenience method, returning a ``ValuesListQuerySet`` (basically
        just an iterable) containing the name of each tag as a string::

            >>> apple.tags.names()
            [u'green and juicy', u'red']

    .. method:: slugs()

        Convenience method, returning a ``ValuesListQuerySet`` (basically
        just an iterable) containing the slug of each tag as a string::

            >>> apple.tags.slugs()
            [u'green-and-juicy', u'red']

    .. hint::

       You can subclass ``_TaggableManager`` (note the underscore) to add
       methods or functionality. ``TaggableManager`` takes an optional
       manager keyword argument for your custom class, like this::

          class Food(models.Model):
              # ... fields here
              tags = TaggableManager(manager=_CustomTaggableManager)

Filtering
~~~~~~~~~

To find all of a model with a specific tags you can filter, using the normal
Django ORM API.  For example if you had a ``Food`` model, whose
``TaggableManager`` was named ``tags``, you could find all the delicious fruit
like so::

    >>> Food.objects.filter(tags__name__in=["delicious"])
    [<Food: apple>, <Food: pear>, <Food: plum>]


If you're filtering on multiple tags, it's very common to get duplicate
results, because of the way relational databases work.  Often you'll want to
make use of the ``distinct()`` method on ``QuerySets``::

    >>> Food.objects.filter(tags__name__in=["delicious", "red"])
    [<Food: apple>, <Food: apple>]
    >>> Food.objects.filter(tags__name__in=["delicious", "red"]).distinct()
    [<Food: apple>]

You can also filter by the slug on tags.  If you're using a custom ``Tag``
model you can use this API to filter on any fields it has.
