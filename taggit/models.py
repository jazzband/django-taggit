from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.template.defaultfilters import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class TaggedItem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, related_name="items")
    content_object = GenericForeignKey()
    
    tag = models.ForeignKey(Tag, related_name="items")
    
    def __unicode__(self):
        return "%s tagged with %s" % (self.content_object, self.tag)
