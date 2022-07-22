Frequently Asked Questions
==========================

- How can I get all my tags?

 If you are using just an out-of-the-box setup, your tags are stored in the `Tag` model (found in `taggit.models`). If this is a custom model (for example you have your own models derived from `ItemBase`), then you'll need to query that one instead.

 So if you are using the standard setup, ``Tag.objects.all()`` will give you the tags.

 - How can I use this with factory_boy?

 Since these are all built off of many-to-many relationships, you can check out `factory_boy's documentation on this topic <https://factoryboy.readthedocs.io/en/stable/recipes.html#simple-many-to-many-relationship>`_ and get some ideas on how to deal with tags.


 One way to handle this is with post-generation hooks::

   class ProductFactory(DjangoModelFactory):
        # Rest of the stuff

        @post_generation
        def tags(self, create, extracted, **kwargs):
            if not create:
                return

            if extracted:
                self.tags.add(*extracted)
