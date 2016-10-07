from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from taggit.models import Tag, TaggedItem


def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    tag = get_object_or_404(Tag, slug=slug)
    qs = queryset.filter(pk__in=TaggedItem.objects.filter(
        tag=tag, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    return ListView.as_view(request, qs, **kwargs)


class TagListMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        self.tag = get_object_or_404(Tag, slug=slug)
        return super(TagListMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        qs = super(TagListMixin, self).get_queryset(**kwargs)
        return qs.filter(
            pk__in=TaggedItem.objects.filter(
                tag=self.tag, content_type=ContentType.objects.get_for_model(qs.model)
            ).values_list("object_id", flat=True))

    def get_template_names(self):
        self.template_name_suffix = '_tag' + self.template_name_suffix
        return super(TagListMixin, self).get_template_names()
