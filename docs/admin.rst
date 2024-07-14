Using tags in the admin
=======================

By default if you have a :class:`TaggableManager` on your model it will show up
in the admin, just as it will in any other form.

If you are specifying :attr:`ModelAdmin.fieldsets
<django.contrib.admin.ModelAdmin.fieldsets>`, include the name of the
:class:`TaggableManager` as a field::

    fieldsets = (
        (None, {'fields': ('tags',)}),
    )

Including tags in ``ModelAdmin.list_display``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One important thing to note is that you *cannot* include a
:class:`TaggableManager` in :attr:`ModelAdmin.list_display
<django.contrib.admin.ModelAdmin.list_display>`. If you do you'll see an
exception that looks like::

    AttributeError: '_TaggableManager' object has no attribute 'name'

This is for the same reason that you cannot include a
:class:`~django.db.models.ManyToManyField`: it would result in an unreasonable
number of queries being executed.

If you want to show tags in :attr:`ModelAdmin.list_display
<django.contrib.admin.ModelAdmin.list_display>`, you can add a custom display
method to the :class:`~django.contrib.admin.ModelAdmin`, using
:meth:`~django.db.models.query.QuerySet.prefetch_related` to minimize queries::

    class MyModelAdmin(admin.ModelAdmin):
        list_display = ['tag_list']

        def get_queryset(self, request):
            return super().get_queryset(request).prefetch_related('tags')

        def tag_list(self, obj):
            return u", ".join(o.name for o in obj.tags.all())


Merging tags in the admin
=======================

Functionality has been added to the admin app to allow for tag "merging". 
Really what is happening is a "find and replace" where the selected tags are being used.

To merge your tags follow these steps:

1. Navigate to the Tags page inside of the Taggit app
2. Select the tags that you want to merge
3. Use the dropdown action list and select `Merge selected tags` and then click `Go`
4. This will redirect you onto a new page where you can insert the new tag name.
5. Click `Merge Tags`
6. This will redirect you back to the tag list