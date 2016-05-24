from __future__ import unicode_literals

from operator import attrgetter

from django import VERSION
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models, router
from django.db.models import signals
from django.db.models.fields import Field
from django.db.models.fields.related import (ManyToManyRel, OneToOneRel,
                                             RelatedField)
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField
from taggit.models import CommonGenericTaggedItemBase, TaggedItem
from taggit.utils import (_get_field, _related_model, _remote_field,
                          require_instance_manager)

if VERSION < (1, 8):
    # related.py was removed in Django 1.8

    # Depending on how Django was updated, related.py could still exist
    # on the users system even on Django 1.8+, so we check the Django
    # version before importing it to make sure this doesn't get imported
    # accidentally.
    from django.db.models.related import RelatedObject
else:
    RelatedObject = None


if VERSION >= (1, 9):
    from django.db.models.fields.related import lazy_related_operation
else:
    from django.db.models.fields.related import add_lazy_relation


try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:  # django < 1.7
    from django.contrib.contenttypes.generic import GenericRelation

try:
    from django.db.models.query_utils import PathInfo
except ImportError:  # Django < 1.8
    try:
        from django.db.models.related import PathInfo
    except ImportError:
        pass  # PathInfo is not used on Django < 1.6


def _model_name(model):
    if VERSION < (1, 6):
        return model._meta.module_name
    else:
        return model._meta.model_name


class TaggableRel(ManyToManyRel):
    def __init__(self, field, related_name, through, to=None):
        # rel.to renamed to rel.model in Django 1.9
        if VERSION >= (1, 9):
            self.model = to
        else:
            self.to = to
        self.related_name = related_name
        self.limit_choices_to = {}
        self.symmetrical = True
        self.multiple = True
        self.through = None if VERSION < (1, 7) else through
        self.field = field
        self.through_fields = None

    def get_joining_columns(self):
        return self.field.get_reverse_joining_columns()

    def get_extra_restriction(self, where_class, alias, related_alias):
        return self.field.get_extra_restriction(where_class, related_alias, alias)


class ExtraJoinRestriction(object):
    """
    An extra restriction used for contenttype restriction in joins.
    """
    contains_aggregate = False

    def __init__(self, alias, col, content_types):
        self.alias = alias
        self.col = col
        self.content_types = content_types

    def as_sql(self, qn, connection):
        # qn changed from a quoting function to be a compiler object in 1.8,
        # which has a quote function
        if VERSION >= (1, 8):
            qn = qn.quote_name_unless_alias
        if len(self.content_types) == 1:
            extra_where = "%s.%s = %%s" % (qn(self.alias), qn(self.col))
        else:
            extra_where = "%s.%s IN (%s)" % (qn(self.alias), qn(self.col),
                                             ','.join(['%s'] * len(self.content_types)))
        return extra_where, self.content_types

    def relabel_aliases(self, change_map):
        self.alias = change_map.get(self.alias, self.alias)

    def clone(self):
        return self.__class__(self.alias, self.col, self.content_types[:])


class _TaggableManager(models.Manager):
    def __init__(self, through, model, instance, prefetch_cache_name):
        self.through = through
        self.model = model
        self.instance = instance
        self.prefetch_cache_name = prefetch_cache_name
        self._db = None

    def is_cached(self, instance):
        return self.prefetch_cache_name in instance._prefetched_objects_cache

    def get_queryset(self, extra_filters=None):
        try:
            return self.instance._prefetched_objects_cache[self.prefetch_cache_name]
        except (AttributeError, KeyError):
            kwargs = extra_filters if extra_filters else {}
            return self.through.tags_for(self.model, self.instance, **kwargs)

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is not None:
            raise ValueError("Custom queryset can't be used for this lookup.")

        instance = instances[0]
        from django.db import connections
        db = self._db or router.db_for_read(instance.__class__, instance=instance)

        fieldname = ('object_id' if issubclass(self.through, CommonGenericTaggedItemBase)
                     else 'content_object')
        fk = self.through._meta.get_field(fieldname)
        query = {
            '%s__%s__in' % (self.through.tag_relname(), fk.name):
                set(obj._get_pk_val() for obj in instances)
        }
        join_table = self.through._meta.db_table
        source_col = fk.column
        connection = connections[db]
        qn = connection.ops.quote_name
        qs = self.get_queryset(query).using(db).extra(
            select={
                '_prefetch_related_val': '%s.%s' % (qn(join_table), qn(source_col))
            }
        )
        return (qs,
                attrgetter('_prefetch_related_val'),
                lambda obj: obj._get_pk_val(),
                False,
                self.prefetch_cache_name)

    # Django < 1.6 uses the previous name of query_set
    get_query_set = get_queryset
    get_prefetch_query_set = get_prefetch_queryset

    def _lookup_kwargs(self):
        return self.through.lookup_kwargs(self.instance)

    @require_instance_manager
    def add(self, *tags):
        db = router.db_for_write(self.through, instance=self.instance)

        tag_objs = self._to_tag_model_instances(tags)
        new_ids = set(t.pk for t in tag_objs)

        # NOTE: can we hardcode 'tag_id' here or should the column name be got
        # dynamically from somewhere?
        vals = (self.through._default_manager.using(db)
                .values_list('tag_id', flat=True)
                .filter(**self._lookup_kwargs()))

        new_ids = new_ids - set(vals)

        signals.m2m_changed.send(
            sender=self.through, action="pre_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )

        for tag in tag_objs:
            self.through._default_manager.using(db).get_or_create(
                tag=tag, **self._lookup_kwargs())

        signals.m2m_changed.send(
            sender=self.through, action="post_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )

    def _to_tag_model_instances(self, tags):
        """
        Takes an iterable containing either strings, tag objects, or a mixture
        of both and returns set of tag objects.
        """
        db = router.db_for_write(self.through, instance=self.instance)

        str_tags = set()
        tag_objs = set()

        for t in tags:
            if isinstance(t, self.through.tag_model()):
                tag_objs.add(t)
            elif isinstance(t, six.string_types):
                str_tags.add(t)
            else:
                raise ValueError(
                    "Cannot add {0} ({1}). Expected {2} or str.".format(
                        t, type(t), type(self.through.tag_model())))

        if getattr(settings, 'TAGGIT_CASE_INSENSITIVE', False):
            # Some databases can do case-insensitive comparison with IN, which
            # would be faster, but we can't rely on it or easily detect it.
            existing = []
            tags_to_create = []

            for name in str_tags:
                try:
                    tag = (self.through.tag_model()._default_manager
                           .using(db)
                           .get(name__iexact=name))
                    existing.append(tag)
                except self.through.tag_model().DoesNotExist:
                    tags_to_create.append(name)
        else:
            # If str_tags has 0 elements Django actually optimizes that to not
            # do a query.  Malcolm is very smart.
            existing = (self.through.tag_model()._default_manager
                        .using(db)
                        .filter(name__in=str_tags))

            tags_to_create = str_tags - set(t.name for t in existing)

        tag_objs.update(existing)

        for new_tag in tags_to_create:
            tag_objs.add(
                self.through.tag_model()._default_manager
                .using(db)
                .create(name=new_tag))

        return tag_objs

    @require_instance_manager
    def names(self):
        return self.get_queryset().values_list('name', flat=True)

    @require_instance_manager
    def slugs(self):
        return self.get_queryset().values_list('slug', flat=True)

    @require_instance_manager
    def set(self, *tags, **kwargs):
        """
        Set the object's tags to the given n tags. If the clear kwarg is True
        then all existing tags are removed (using `.clear()`) and the new tags
        added. Otherwise, only those tags that are not present in the args are
        removed and any new tags added.
        """
        db = router.db_for_write(self.through, instance=self.instance)
        clear = kwargs.pop('clear', False)

        if clear:
            self.clear()
            self.add(*tags)
        else:
            # make sure we're working with a collection of a uniform type
            objs = self._to_tag_model_instances(tags)

            # get the existing tag strings
            old_tag_strs = set(self.through._default_manager
                               .using(db)
                               .filter(**self._lookup_kwargs())
                               .values_list('tag__name', flat=True))

            new_objs = []
            for obj in objs:
                if obj.name in old_tag_strs:
                    old_tag_strs.remove(obj.name)
                else:
                    new_objs.append(obj)

        self.remove(*old_tag_strs)
        self.add(*new_objs)

    @require_instance_manager
    def remove(self, *tags):
        if not tags:
            return

        db = router.db_for_write(self.through, instance=self.instance)

        qs = (self.through._default_manager.using(db)
              .filter(**self._lookup_kwargs())
              .filter(tag__name__in=tags))

        old_ids = set(qs.values_list('tag_id', flat=True))

        signals.m2m_changed.send(
            sender=self.through, action="pre_remove",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=old_ids, using=db,
        )
        qs.delete()
        signals.m2m_changed.send(
            sender=self.through, action="post_remove",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=old_ids, using=db,
        )

    @require_instance_manager
    def clear(self):
        db = router.db_for_write(self.through, instance=self.instance)

        signals.m2m_changed.send(
            sender=self.through, action="pre_clear",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=None, using=db,
        )

        self.through._default_manager.using(db).filter(
            **self._lookup_kwargs()).delete()

        signals.m2m_changed.send(
            sender=self.through, action="post_clear",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=None, using=db,
        )

    def most_common(self, min_count=None):
        queryset = self.get_queryset().annotate(
            num_times=models.Count(self.through.tag_relname())
        ).order_by('-num_times')
        if min_count:
            queryset = queryset.filter(num_times__gte=min_count)

        return queryset

    @require_instance_manager
    def similar_objects(self):
        lookup_kwargs = self._lookup_kwargs()
        lookup_keys = sorted(lookup_kwargs)
        qs = self.through.objects.values(*six.iterkeys(lookup_kwargs))
        qs = qs.annotate(n=models.Count('pk'))
        qs = qs.exclude(**lookup_kwargs)
        qs = qs.filter(tag__in=self.all())
        qs = qs.order_by('-n')

        # TODO: This all feels like a bit of a hack.
        items = {}
        if len(lookup_keys) == 1:
            # Can we do this without a second query by using a select_related()
            # somehow?
            f = _get_field(self.through, lookup_keys[0])
            remote_field = _remote_field(f)
            rel_model = _related_model(_remote_field(f))
            objs = rel_model._default_manager.filter(**{
                "%s__in" % remote_field.field_name: [r["content_object"] for r in qs]
            })
            for obj in objs:
                items[(getattr(obj, remote_field.field_name),)] = obj
        else:
            preload = {}
            for result in qs:
                preload.setdefault(result['content_type'], set())
                preload[result["content_type"]].add(result["object_id"])

            for ct, obj_ids in preload.items():
                ct = ContentType.objects.get_for_id(ct)
                for obj in ct.model_class()._default_manager.filter(pk__in=obj_ids):
                    items[(ct.pk, obj.pk)] = obj

        results = []
        for result in qs:
            obj = items[
                tuple(result[k] for k in lookup_keys)
            ]
            obj.similar_tags = result["n"]
            results.append(obj)
        return results

    # _TaggableManager needs to be hashable but BaseManagers in Django 1.8+ overrides
    # the __eq__ method which makes the default __hash__ method disappear.
    # This checks if the __hash__ attribute is None, and if so, it reinstates the original method.
    if models.Manager.__hash__ is None:
        __hash__ = object.__hash__


class TaggableManager(RelatedField, Field):
    # Field flags
    many_to_many = True
    many_to_one = False
    one_to_many = False
    one_to_one = False

    _related_name_counter = 0

    def __init__(self, verbose_name=_("Tags"),
                 help_text=_("A comma-separated list of tags."),
                 through=None, blank=False, related_name=None, to=None,
                 manager=_TaggableManager):

        self.through = through or TaggedItem
        self.swappable = False
        self.manager = manager

        rel = TaggableRel(self, related_name, self.through, to=to)

        Field.__init__(
            self,
            verbose_name=verbose_name,
            help_text=help_text,
            blank=blank,
            null=True,
            serialize=False,
            rel=rel,
        )
        # NOTE: `to` is ignored, only used via `deconstruct`.

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                             "before you can access their tags." % model.__name__)
        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            prefetch_cache_name=self.name
        )
        return manager

    def deconstruct(self):
        """
        Deconstruct the object, used with migrations.
        """
        name, path, args, kwargs = super(TaggableManager, self).deconstruct()
        # Remove forced kwargs.
        for kwarg in ('serialize', 'null'):
            del kwargs[kwarg]
        # Add arguments related to relations.
        # Ref: https://github.com/alex/django-taggit/issues/206#issuecomment-37578676
        rel = _remote_field(self)
        if isinstance(rel.through, six.string_types):
            kwargs['through'] = rel.through
        elif not rel.through._meta.auto_created:
            kwargs['through'] = "%s.%s" % (rel.through._meta.app_label, rel.through._meta.object_name)

        related_model = _related_model(rel)
        if isinstance(related_model, six.string_types):
            kwargs['to'] = related_model
        else:
            kwargs['to'] = '%s.%s' % (related_model._meta.app_label, related_model._meta.object_name)

        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        if VERSION < (1, 7):
            self.name = self.column = self.attname = name
        else:
            self.set_attributes_from_name(name)
        self.model = cls
        self.opts = cls._meta

        cls._meta.add_field(self)
        setattr(cls, name, self)
        if not cls._meta.abstract:
            # rel.to renamed to remote_field.model in Django 1.9
            if VERSION >= (1, 9):
                if isinstance(self.remote_field.model, six.string_types):
                    def resolve_related_class(cls, model, field):
                        field.remote_field.model = model
                    lazy_related_operation(
                        resolve_related_class, cls, self.remote_field.model, field=self
                    )
            else:
                if isinstance(self.rel.to, six.string_types):
                    def resolve_related_class(field, model, cls):
                        field.rel.to = model
                    add_lazy_relation(cls, self, self.rel.to, resolve_related_class)

            if isinstance(self.through, six.string_types):
                if VERSION >= (1, 9):
                    def resolve_related_class(cls, model, field):
                        self.through = model
                        self.remote_field.through = model
                        self.post_through_setup(cls)
                    lazy_related_operation(
                        resolve_related_class, cls, self.through, field=self
                    )
                else:
                    def resolve_related_class(field, model, cls):
                        self.through = model
                        _remote_field(self).through = model
                        self.post_through_setup(cls)
                    add_lazy_relation(
                        cls, self, self.through, resolve_related_class
                    )
            else:
                self.post_through_setup(cls)

    def get_internal_type(self):
        return 'ManyToManyField'

    def __lt__(self, other):
        """
        Required contribute_to_class as Django uses bisect
        for ordered class contribution and bisect requires
        a orderable type in py3.
        """
        return False

    def post_through_setup(self, cls):
        if RelatedObject is not None:  # Django < 1.8
            self.related = RelatedObject(cls, self.model, self)

        self.use_gfk = (
            self.through is None or issubclass(self.through, CommonGenericTaggedItemBase)
        )

        # rel.to renamed to remote_field.model in Django 1.9
        if VERSION >= (1, 9):
            if not self.remote_field.model:
                self.remote_field.model = self.through._meta.get_field("tag").remote_field.model
        else:
            if not self.rel.to:
                self.rel.to = self.through._meta.get_field("tag").rel.to

        if RelatedObject is not None:  # Django < 1.8
            self.related = RelatedObject(self.through, cls, self)

        if self.use_gfk:
            tagged_items = GenericRelation(self.through)
            tagged_items.contribute_to_class(cls, 'tagged_items')

        for rel in cls._meta.local_many_to_many:
            if rel == self or not isinstance(rel, TaggableManager):
                continue
            if rel.through == self.through:
                raise ValueError('You can\'t have two TaggableManagers with the'
                                 ' same through model.')

    def save_form_data(self, instance, value):
        getattr(instance, self.name).set(*value)

    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank
        }
        defaults.update(kwargs)
        return form_class(**defaults)

    def value_from_object(self, instance):
        if instance.pk:
            return self.through.objects.filter(**self.through.lookup_kwargs(instance))
        return self.through.objects.none()

    def related_query_name(self):
        return _model_name(self.model)

    def m2m_reverse_name(self):
        return _get_field(self.through, 'tag').column

    def m2m_reverse_field_name(self):
        return _get_field(self.through, 'tag').name

    def m2m_target_field_name(self):
        return self.model._meta.pk.name

    def m2m_reverse_target_field_name(self):
        # rel.to renamed to remote_field.model in Django 1.9
        if VERSION >= (1, 9):
            return self.remote_field.model._meta.pk.name
        else:
            return self.rel.to._meta.pk.name

    def m2m_column_name(self):
        if self.use_gfk:
            return self.through._meta.virtual_fields[0].fk_field
        return self.through._meta.get_field('content_object').column

    def db_type(self, connection=None):
        return None

    def m2m_db_table(self):
        return self.through._meta.db_table

    def bulk_related_objects(self, new_objs, using):
        return []

    def extra_filters(self, pieces, pos, negate):
        if negate or not self.use_gfk:
            return []
        prefix = "__".join(["tagged_items"] + pieces[:pos - 2])
        get = ContentType.objects.get_for_model
        cts = [get(obj) for obj in _get_subclasses(self.model)]
        if len(cts) == 1:
            return [("%s__content_type" % prefix, cts[0])]
        return [("%s__content_type__in" % prefix, cts)]

    def get_extra_join_sql(self, connection, qn, lhs_alias, rhs_alias):
        model_name = _model_name(self.through)
        if rhs_alias == '%s_%s' % (self.through._meta.app_label, model_name):
            alias_to_join = rhs_alias
        else:
            alias_to_join = lhs_alias
        extra_col = _get_field(self.through, 'content_type').column
        content_type_ids = [ContentType.objects.get_for_model(subclass).pk for
                            subclass in _get_subclasses(self.model)]
        if len(content_type_ids) == 1:
            content_type_id = content_type_ids[0]
            extra_where = " AND %s.%s = %%s" % (qn(alias_to_join),
                                                qn(extra_col))
            params = [content_type_id]
        else:
            extra_where = " AND %s.%s IN (%s)" % (qn(alias_to_join),
                                                  qn(extra_col),
                                                  ','.join(['%s'] *
                                                           len(content_type_ids)))
            params = content_type_ids
        return extra_where, params

    # This and all the methods till the end of class are only used in django >= 1.6
    def _get_mm_case_path_info(self, direct=False):
        pathinfos = []
        linkfield1 = _get_field(self.through, 'content_object')
        linkfield2 = _get_field(self.through, self.m2m_reverse_field_name())
        if direct:
            join1infos = linkfield1.get_reverse_path_info()
            join2infos = linkfield2.get_path_info()
        else:
            join1infos = linkfield2.get_reverse_path_info()
            join2infos = linkfield1.get_path_info()
        pathinfos.extend(join1infos)
        pathinfos.extend(join2infos)
        return pathinfos

    def _get_gfk_case_path_info(self, direct=False):
        pathinfos = []
        from_field = self.model._meta.pk
        opts = self.through._meta
        linkfield = _get_field(self.through, self.m2m_reverse_field_name())
        if direct:
            join1infos = [PathInfo(self.model._meta, opts, [from_field], _remote_field(self), True, False)]
            join2infos = linkfield.get_path_info()
        else:
            join1infos = linkfield.get_reverse_path_info()
            join2infos = [PathInfo(opts, self.model._meta, [from_field], self, True, False)]
        pathinfos.extend(join1infos)
        pathinfos.extend(join2infos)
        return pathinfos

    def get_path_info(self):
        if self.use_gfk:
            return self._get_gfk_case_path_info(direct=True)
        else:
            return self._get_mm_case_path_info(direct=True)

    def get_reverse_path_info(self):
        if self.use_gfk:
            return self._get_gfk_case_path_info(direct=False)
        else:
            return self._get_mm_case_path_info(direct=False)

    def get_joining_columns(self, reverse_join=False):
        if reverse_join:
            return ((self.model._meta.pk.column, "object_id"),)
        else:
            return (("object_id", self.model._meta.pk.column),)

    def get_extra_restriction(self, where_class, alias, related_alias):
        extra_col = _get_field(self.through, 'content_type').column
        content_type_ids = [ContentType.objects.get_for_model(subclass).pk
                            for subclass in _get_subclasses(self.model)]
        return ExtraJoinRestriction(related_alias, extra_col, content_type_ids)

    def get_reverse_joining_columns(self):
        return self.get_joining_columns(reverse_join=True)

    @property
    def related_fields(self):
        return [(_get_field(self.through, 'object_id'), self.model._meta.pk)]

    @property
    def foreign_related_fields(self):
        return [self.related_fields[0][1]]


def _get_subclasses(model):
    subclasses = [model]
    if VERSION < (1, 8):
        all_fields = (_get_field(model, f) for f in model._meta.get_all_field_names())
    else:
        all_fields = model._meta.get_fields()
    for field in all_fields:
        # Django 1.8 +
        if (not RelatedObject and isinstance(field, OneToOneRel) and
                getattr(_remote_field(field.field), "parent_link", None)):
            subclasses.extend(_get_subclasses(field.related_model))

        # < Django 1.8
        if (RelatedObject and isinstance(field, RelatedObject) and
                getattr(field.field.rel, "parent_link", None)):
            subclasses.extend(_get_subclasses(field.model))
    return subclasses


# `total_ordering` does not exist in Django 1.4, as such
# we special case this import to be py3k specific which
# is not supported by Django 1.4
if six.PY3:
    from django.utils.functional import total_ordering
    TaggableManager = total_ordering(TaggableManager)
