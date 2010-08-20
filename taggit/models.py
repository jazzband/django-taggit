import django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext


class Tag(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.name)
            if django.VERSION >= (1, 2):
                from django.db import router
                using = kwargs.get("using") or router.db_for_write(
                    type(self), instance=self)
                # Make sure we write to the same db for all attempted writes,
                # with a multi-master setup, theoretically we could try to
                # write and rollback on different DBs
                kwargs["using"] = using
                trans_kwargs = {"using": using}
            else:
                trans_kwargs = {}
            i = 0
            while True:
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(Tag, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
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
        return ugettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag
        }
    
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
    object_id = models.IntegerField(verbose_name=_('Object id'), db_index=True)
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'),
        related_name="tagged_items")
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
        
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

