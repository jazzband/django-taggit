from django.contrib.contenttypes.models import ContentType
from django.db import models

from taggit.models import Tag, TaggedItem
from taggit.utils import require_instance_manager


class TaggableManager(object):
    def __get__(self, instance, type):
        manager = _TaggableManager()
        manager.model = type
        if instance is None:
            manager.object_id = None
        else:
            manager.object_id = instance.pk
        return manager


class _TaggableManager(models.Manager):
    def get_query_set(self):
        ct = ContentType.objects.get_for_model(self.model)
        if self.object_id is not None:
            return Tag.objects.filter(items__object_id=self.object_id, 
                items__content_type=ct)
        else:
            return Tag.objects.filter(items__content_type=ct).distinct()
    
    @require_instance_manager
    def add(self, tags):
        if isinstance(tags, basestring):
            tags = [tags]
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(name=tag)
            TaggedItem.objects.create(object_id=self.object_id, 
                content_type=ContentType.objects.get_for_model(self.model), tag=tag)
    
    @require_instance_manager
    def set(self, tags):
        self.clear()
        self.add(tags)
    
    @require_instance_manager
    def remove(self, tags):
        if isinstance(tags, basestring):
            tags = [tags]
        TaggedItem.objects.filter(object_id=self.object_id, 
            content_type=ContentType.objects.get_for_model(self.model)).filter(
            tag__name__in=tags).delete()
    
    @require_instance_manager
    def clear(self):
        TaggedItem.objects.filter(object_id=self.object_id,
            content_type=ContentType.objects.get_for_model(self.model)).delete()
