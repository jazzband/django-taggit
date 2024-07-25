Testing
=======

Natural Key Support
-------------------
We have added `natural key support <https://docs.djangoproject.com/en/5.0/topics/serialization/#natural-keys>`_ to the Tag model in the Django taggit library. This allows you to identify objects by human-readable identifiers rather than by their database ID::

    python manage.py dumpdata taggit.Tag --natural-foreign --natural-primary > tags.json

    python manage.py loaddata tags.json

By default tags use the name field as the natural key.

You can customize this in your own custom tag model by setting the ``natural_key_fields`` property on your model the required fields.
