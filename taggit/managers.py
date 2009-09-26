from django.contrib.contenttypes.models import ContentType
from django.db import models

from taggit.models import Tag, TaggedItem
from tagging.utils import require_instance_manager


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
            return Tag.objects.filter(items__content_type=ct)
    
    @require_instance_manager
    def add_tag(self, tag):
        tag, _ = Tag.objects.get_or_create(name=tag)
        TaggedItem.objects.create(object_id=self.object_id, 
            content_type=ContentType.objects.get_for_model(self.model), tag=tag)
    
    @require_instance_manager
    def add_tags(self, tags):
        for tag in tags:
            self.add_tag(tag)
    
    @require_instance_manager
    def set_tags(self, tags):
        self.clear_tags()
        self.add_tags(tags)
    
    @require_instance_manager
    def clear_tags(self):
        TaggedItem.objects.filter(object_id=self.object_id,
            content_type=ContentType.objects.get_for_model(self.model)).delete()
