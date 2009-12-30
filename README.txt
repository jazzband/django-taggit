django-taggit
=============

Is a simpler approach to tagging with Django.  Just add a TaggableManager to your
model and go:
    
    from django.db import models
    
    from taggit.managers import TaggableManager
    
    class Food(models.Model):
        # ... fields here
        
        tags = TaggableManager()
    

Then you can use the API like so:
    
    >>> apple = Food.objects.create(name="apple")
    >>> apple.tags.add("red", "green", "delicious")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: green>, <Tag: delicious>]
    >>> apple.tags.remove("green")
    [<Tag: red>, <Tag: delicious>]
    >>> Food.objects.filter(tags="red")
    [<Food: apple>, <Food: cherry>]


Tags will show up for you automatically in forms and the admin.
