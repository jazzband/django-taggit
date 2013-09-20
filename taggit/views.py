from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from taggit.models import TaggedItem, Tag


class TaggedObjectList(ListView):
    """Show all objects with a given tag.

    The URLconf has to capture a parameter `slug` or pass it as additional
    keyword argument.
    """

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])

        queryset = super(TaggedObjectList, self).get_queryset()
        queryset = queryset.filter(pk__in=TaggedItem.objects.filter(
            tag=self.tag, content_type=ContentType.objects.get_for_model(queryset.model)
        ).values_list("object_id", flat=True))

        return queryset

    def get_context_data(self, **kwargs):
        context = {'tag': self.tag}
        context.update(kwargs)
        return super(TaggedObjectList, self).get_context_data(**context)
