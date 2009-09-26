from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name


class TaggedItem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey()
    
    tag = models.ForeignKey(Tag, related_name="items")
    
    def __unicode__(self):
        return "%s tagged with %" % (self.content_object, self.tag)
