from __future__ import unicode_literals

import django
from django import VERSION
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models, transaction
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify as default_slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from taggit.utils import _get_field

try:
    from unidecode import unidecode
except ImportError:
    def unidecode(tag):
        return tag


try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:  # django < 1.7
    from django.contrib.contenttypes.generic import GenericForeignKey


try:
    atomic = transaction.atomic
except AttributeError:
    from contextlib import contextmanager

    @contextmanager
    def atomic(using=None):
        sid = transaction.savepoint(using=using)
        try:
            yield
        except IntegrityError:
            transaction.savepoint_rollback(sid, using=using)
            raise
        else:
            transaction.savepoint_commit(sid, using=using)


@python_2_unicode_compatible
class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            from django.db import router
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self)
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be oportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with atomic(using=using):
                    res = super(TagBase, self).save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(
                self.__class__._default_manager
                .filter(slug__startswith=self.slug)
                .values_list('slug', flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrecny issues here for now.
                    # (That is, till we found a nice solution...)
                    return super(TagBase, self).save(*args, **kwargs)
                i += 1
        else:
            return super(TagBase, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = default_slugify(unidecode(tag))
        if i is not None:
            slug += "_%d" % i
        return slug


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
        field = _get_field(cls, 'tag')
        return field.remote_field.model if VERSION >= (1, 9) else field.rel.to

    @classmethod
    def tag_relname(cls):
        field = _get_field(cls, 'tag')
        return field.remote_field.related_name if VERSION >= (1, 9) else field.rel.related_name

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
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({
                '%s__content_object' % cls.tag_relname(): instance
            })
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update({
            '%s__content_object__isnull' % cls.tag_relname(): False
        })
        return cls.tag_model().objects.filter(**kwargs).distinct()


class CommonGenericTaggedItemBase(ItemBase):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
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
    def tags_for(cls, model, instance=None, **extra_filters):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        if extra_filters:
            kwargs.update(extra_filters)
        return cls.tag_model().objects.filter(**kwargs).distinct()


class GenericTaggedItemBase(CommonGenericTaggedItemBase):
    object_id = models.IntegerField(verbose_name=_('Object id'), db_index=True)

    class Meta:
        abstract = True


if VERSION >= (1, 8):

    class GenericUUIDTaggedItemBase(CommonGenericTaggedItemBase):
        object_id = models.UUIDField(verbose_name=_('Object id'), db_index=True)

        class Meta:
            abstract = True


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
        if django.VERSION >= (1, 5):
            index_together = [
                ["content_type", "object_id"],
            ]
