Known Issues
============

Currently there is 1 known issue:

 * When run under Django 1.1, doing ``Model.objects.all().delete()`` (or any
   bulk deletion operation) on a model with a ``TaggableManager`` will result
   in losing the tags for items beyond just those assosciated with the deleted
   objects.  This issue is not present in Django 1.2.
