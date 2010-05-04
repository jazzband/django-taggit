from collections import defaultdict

import django
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.related import ManyToManyRel
from django.db.models.related import RelatedObject
from django.db.models.query_utils import QueryWrapper

from taggit.forms import TagField
from taggit.models import Tag, TaggedItem
from taggit.utils import require_instance_manager



class TaggableRel(ManyToManyRel):
    def __init__(self, to):
        self.to = to
        self.related_name = None
        self.limit_choices_to = {}
        self.symmetrical = True
        self.multiple = True
        self.through = None


class TaggableManager(object):
    def __init__(self, verbose_name="Tags", through=None):
        self.use_gfk = through is None
        self.through = through or TaggedItem
        self.rel = TaggableRel(to=self.through)
        self.verbose_name = verbose_name
        self.editable = True
        self.unique = False
        self.creates_table = False
        self.db_column = None
        self.choices = None
        self.serialize = False
        self.creation_counter = models.Field.creation_counter
        models.Field.creation_counter += 1

    def __get__(self, instance, model):
        manager = _TaggableManager(through=self.through)
        manager.model = model
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their tags." % model.__name__)
        manager.instance = instance
        return manager

    def contribute_to_class(self, cls, name):
        self.name = self.column = name
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, name, self)

    def save_form_data(self, instance, value):
        getattr(instance, self.name).set(*value)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type !=  "in":
            raise ValueError("You can't do lookups other than \"in\" on Tags")
        if all(isinstance(v, Tag) for v in value):
            qs = self.through.objects.filter(tag__in=value)
        elif all(isinstance(v, basestring) for v in value):
            qs = self.through.objects.filter(tag__name__in=value)
        elif all(isinstance(v, (int, long)) for v in value):
            # This one is really ackward, just don't do it.  The ORM does it
            # for deletes, but no one else gets to.
            return value
        else:
            # Fucking flip-floppers.
            raise ValueError("You can't combine Tag objects and strings. '%s' was provided." % value)
        if hasattr(models.Field, "get_prep_lookup"):
            return models.Field().get_prep_lookup(lookup_type, qs)
        return models.Field().get_db_prep_lookup(lookup_type, qs)
    
    if django.VERSION < (1, 2):
        get_db_prep_lookup = get_prep_lookup
    else:
        def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
            if not prepared:
                return self.get_prep_lookup(lookup_type, value)
            return models.Field().get_db_prep_lookup(lookup_type, value, connection=connection, prepared=True)

    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": "Tags",
            "help_text": "A comma-separated list of tags."
        }
        defaults.update(kwargs)
        return form_class(**kwargs)

    def value_from_object(self, instance):
        if instance.pk:
            return self.through.objects.filter(**self.through.lookup_kwargs(instance))
        return self.through.objects.none()

    def related_query_name(self):
        return None

    def m2m_reverse_name(self):
        if self.use_gfk:
            return "id"
        return self.through._meta.get_field('content_object').rel.to._meta.pk.column

    def m2m_column_name(self):
        if self.use_gfk:
            return self.through._meta.virtual_fields[0].fk_field
        return self.through._meta.get_field('content_object').column

    def db_type(self, connection=None):
        return None

    def m2m_db_table(self):
        return self.through._meta.db_table

    def extra_filters(self, pieces, pos, negate):
        if negate or not self.use_gfk:
            return []
        prefix = "__".join(pieces[:pos+1])
        cts = map(ContentType.objects.get_for_model, _get_subclasses(self.model))
        if len(cts) == 1:
            return [("%s__content_type" % prefix, cts[0])]
        return [("%s__content_type__in" % prefix, cts)]


class _TaggableManager(models.Manager):
    def __init__(self, through):
        self.through = through
        
    def get_query_set(self):
        return self.through.tags_for(self.model, self.instance)

    def _lookup_kwargs(self):
        return self.through.lookup_kwargs(self.instance)
    
    @require_instance_manager
    def add(self, *tags):
        for tag in tags:
            if not isinstance(tag, Tag):
                tag, _ = Tag.objects.get_or_create(name=tag)
            self.through.objects.get_or_create(tag=tag, **self._lookup_kwargs())

    @require_instance_manager
    def set(self, *tags):
        self.clear()
        self.add(*tags)

    @require_instance_manager
    def remove(self, *tags):
        self.through.objects.filter(**self._lookup_kwargs()).filter(
            tag__name__in=tags).delete()

    @require_instance_manager
    def clear(self):
        self.through.objects.filter(**self._lookup_kwargs()).delete()

    def most_common(self):
        return self.get_query_set().annotate(
            num_times=models.Count(self.through.tag_relname())
        ).order_by('-num_times')

    @require_instance_manager
    def similar_objects(self):
        lookup_kwargs = self._lookup_kwargs()
        qs = self.through.objects.values(*lookup_kwargs.keys())
        qs = qs.annotate(n=models.Count('pk'))
        qs = qs.exclude(**lookup_kwargs)
        qs = qs.filter(tag__in=self.all())
        qs = qs.order_by('-n')
        
        # TODO: This all feels like a giant hack... giant.
        if len(lookup_kwargs) == 1:
            using_gfk = False
            # Can this just be select_related?  I think so.
            items = self.through._meta.get_field_by_name(
                lookup_kwargs.keys()[0]
            )[0].rel.to._default_manager.in_bulk(
                [r["content_object"] for r in qs]
            )
        else:
            using_gfk = True
            preload = defaultdict(set)
            for result in qs:
                preload[result["content_type"]].add(result["object_id"])

            items = {}
            for ct, obj_ids in preload.iteritems():
                ct = ContentType.objects.get_for_id(ct)
                items[ct.pk] = ct.model_class()._default_manager.in_bulk(obj_ids)

        results = []
        for result in qs:
            # TODO: Consolidate this into dicts keyed by a tuple of the
            # (content_type, object_id) instead of the nesting.
            if using_gfk:
                obj = items[result["content_type"]][result["object_id"]]
            else:
                obj = items[result["content_object"]]
            obj.similar_tags = result["n"]
            results.append(obj)
        return results


def _get_subclasses(model):
    subclasses = [model]
    for f in model._meta.get_all_field_names():
        field = model._meta.get_field_by_name(f)[0]
        if (isinstance(field, RelatedObject) and
            getattr(field.field.rel, "parent_link", None)):
            subclasses.extend(_get_subclasses(field.model))
    return subclasses
