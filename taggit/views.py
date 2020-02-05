from dal import autocomplete
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from taggit.models import Tag, TaggedItem


def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    kwargs["slug"] = slug
    tag_list_view = type(
        "TagListView",
        (TagListMixin, ListView),
        {"model": queryset.model, "queryset": queryset},
    )
    return tag_list_view.as_view()(request, **kwargs)


class TagListMixin:
    tag_suffix = "_tag"

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.pop("slug")
        self.tag = get_object_or_404(Tag, slug=slug)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(
            pk__in=TaggedItem.objects.filter(
                tag=self.tag, content_type=ContentType.objects.get_for_model(qs.model)
            ).values_list("object_id", flat=True)
        )

    def get_template_names(self):
        if self.tag_suffix:
            self.template_name_suffix = self.tag_suffix + self.template_name_suffix
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "extra_context" not in context:
            context["extra_context"] = {}
        context["extra_context"]["tag"] = self.tag
        return context


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated() or (
                not self.request.user.is_superuser and not self.request.user.has_perm('taggit.change_tag')):
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = Tag.objects.filter(
                Q(name__icontains=self.q) | Q(slug__icontains=self.q)).all()
        return qs
