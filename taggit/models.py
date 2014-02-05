from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import python_2_unicode_compatible
from autoslug import AutoSlugField


@python_2_unicode_compatible
class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), unique=True, max_length=100)
    slug = AutoSlugField(verbose_name=_('Slug'), unique=True, max_length=100,
        populate_from='name', editable=True, sep='_')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Tag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


@python_2_unicode_compatible
class ItemBase(models.Model):
    def __str__(self):
        return ugettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag
        }

    class Meta:
        abstract = True

    @classmethod
    def tag_model(cls):
        return cls._meta.get_field_by_name("tag")[0].rel.to

    @classmethod
    def tag_relname(cls):
        return cls._meta.get_field_by_name('tag')[0].rel.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'content_object': instance
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        return {
            "content_object__in": instances,
        }


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


class GenericTaggedItemBase(ItemBase):
    object_id = models.IntegerField(verbose_name=_('Object id'), db_index=True)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        related_name="%(app_label)s_%(class)s_tagged_items"
    )
    content_object = GenericForeignKey()

    class Meta:
        abstract = True

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        if isinstance(instances, QuerySet):
            # Can do a real object_id IN (SELECT ..) query.
            return {
                "object_id__in": instances,
                "content_type": ContentType.objects.get_for_model(instances.model),
            }
        else:
            # TODO: instances[0], can we assume there are instances.
            return {
                "object_id__in": [instance.pk for instance in instances],
                "content_type": ContentType.objects.get_for_model(instances[0]),
            }

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
