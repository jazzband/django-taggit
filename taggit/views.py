from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from taggit.models import TaggedItem, Tag


def tagged_object_list(request, slug, queryset, through=None, **kwargs):
    if callable(queryset):
        queryset = queryset()
    tag = get_object_or_404(Tag, slug=slug)
    if through is not None:
        qs = queryset.filter(pk__in=through.objects.filter(tag=tag
                ).values_list("content_object_id", flat=True))
    else:
        qs = queryset.filter(pk__in=TaggedItem.objects.filter(tag=tag,
                content_type=ContentType.objects.get_for_model(queryset.model)
                ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    return object_list(request, qs, **kwargs)
