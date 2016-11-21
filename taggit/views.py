from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from taggit.models import Tag, TaggedItem


def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    queryset_model = ContentType.objects.get_for_model(queryset.model)
    kwargs["slug"] = slug
    tag_list_view = type(
        str('TagListView'),
        (TagListMixin, ListView),
        {
            'model': queryset_model,
            'queryset': queryset
        }
    )
    return tag_list_view.as_view()(request, **kwargs)


class TagListMixin(object):
    tag_suffix = '_tag'

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
        if self.tag_suffix:
            self.template_name_suffix = self.tag_suffix + self.template_name_suffix
        return super(TagListMixin, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(TagListMixin, self).get_context_data(**kwargs)
        if "extra_context" not in context:
            context["extra_context"] = {}
        context["extra_context"]["tag"] = self.tag
        return context
