from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models, router, transaction
from django.utils.text import slugify
from django.utils.translation import gettext, gettext_lazy as _

try:
    from unidecode import unidecode
except ImportError:

    def unidecode(tag):
        return tag


class TagBase(models.Model):
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100)

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = self.slugify(self.name)
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self
            )
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be oportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with transaction.atomic(using=using):
                    res = super().save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(
                self.__class__._default_manager.filter(
                    slug__startswith=self.slug
                ).values_list("slug", flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrecny issues here for now.
                    # (That is, till we found a nice solution...)
                    return super().save(*args, **kwargs)
                i += 1
        else:
            return super().save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = slugify(unidecode(tag))
        if i is not None:
            slug += "_%d" % i
        return slug


class Tag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        app_label = "taggit"


class ItemBase(models.Model):
    def __str__(self):
        return gettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag,
        }

    class Meta:
        abstract = True

    @classmethod
    def tag_model(cls):
        field = cls._meta.get_field("tag")
        return field.remote_field.model

    @classmethod
    def tag_relname(cls):
        field = cls._meta.get_field("tag")
        return field.remote_field.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {"content_object": instance}


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(
        Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({"%s__content_object" % cls.tag_relname(): instance})
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update({"%s__content_object__isnull" % cls.tag_relname(): False})
        return cls.tag_model().objects.filter(**kwargs).distinct()


class CommonGenericTaggedItemBase(ItemBase):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content type"),
        related_name="%(app_label)s_%(class)s_tagged_items",
    )
    content_object = GenericForeignKey()

    class Meta:
        abstract = True

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            "object_id": instance.pk,
            "content_type": ContentType.objects.get_for_model(instance),
        }

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        tag_relname = cls.tag_relname()
        kwargs = {
            "%s__content_type__app_label" % tag_relname: model._meta.app_label,
            "%s__content_type__model" % tag_relname: model._meta.model_name,
        }
        if instance is not None:
            kwargs["%s__object_id" % tag_relname] = instance.pk
        if extra_filters:
            kwargs.update(extra_filters)
        return cls.tag_model().objects.filter(**kwargs).distinct()


class GenericTaggedItemBase(CommonGenericTaggedItemBase):
    object_id = models.IntegerField(verbose_name=_("Object id"), db_index=True)

    class Meta:
        abstract = True


class GenericUUIDTaggedItemBase(CommonGenericTaggedItemBase):
    object_id = models.UUIDField(verbose_name=_("Object id"), db_index=True)

    class Meta:
        abstract = True


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
        app_label = "taggit"
        index_together = [["content_type", "object_id"]]
        unique_together = [["content_type", "object_id", "tag"]]
