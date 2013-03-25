from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
#this does not work anymore in django 1.5, see also: https://docs.djangoproject.com/en/1.4/topics/generic-views-migration/
#from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView

from taggit.models import TaggedItem, Tag


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
    #return object_list(request, qs, **kwargs)
    return ListView.as_view(request, qs, **kwargs)

