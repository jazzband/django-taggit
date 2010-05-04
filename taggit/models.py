import django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Tag, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(Tag, self).save(*args, **kwargs)


class TaggedItemBase(models.Model):
    if django.VERSION < (1, 2):
        tag = models.ForeignKey(Tag, related_name="%(class)s_items")
    else:
        tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items")

    def __unicode__(self):
        return "%s tagged with %s" % (self.content_object, self.tag)
    
    class Meta:
        abstract = True

    @classmethod
    def tag_relname(cls):
        return cls._meta.get_field_by_name('tag')[0].rel.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'content_object': instance
        }

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return Tag.objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return Tag.objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


class TaggedItem(TaggedItemBase):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, related_name="tagged_items")
    content_object = GenericForeignKey()

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        if instance is not None:
            return Tag.objects.filter(**{
                '%s__object_id' % cls.tag_relname(): instance.pk,
                '%s__content_type' % cls.tag_relname(): ct
            })
        return Tag.objects.filter(**{
            '%s__content_type' % cls.tag_relname(): ct
        }).distinct()

