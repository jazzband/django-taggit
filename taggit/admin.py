from django.contrib import admin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path

from taggit.models import Tag, TaggedItem

from .forms import MergeTagsForm


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    actions = ["render_tag_form"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "merge-tags/",
                self.admin_site.admin_view(self.merge_tags_view),
                name="taggit_tag_merge_tags",
            ),
        ]
        return custom_urls + urls

    @admin.action(description="Merge selected tags")
    def render_tag_form(self, request, queryset):
        selected = request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)
        if not selected:
            self.message_user(request, "Please select at least one tag.")
            return redirect(request.get_full_path())

        selected_tag_ids = ",".join(selected)
        redirect_url = f"{request.get_full_path()}merge-tags/"

        request.session["selected_tag_ids"] = selected_tag_ids

        return redirect(redirect_url)

    def merge_tags_view(self, request):
        selected_tag_ids = request.session.get("selected_tag_ids", "").split(",")
        if request.method == "POST":
            form = MergeTagsForm(request.POST)
            if form.is_valid():
                new_tag_name = form.cleaned_data["new_tag_name"]
                new_tag, created = Tag.objects.get_or_create(name=new_tag_name)
                with transaction.atomic():
                    for tag_id in selected_tag_ids:
                        tag = Tag.objects.get(id=tag_id)
                        tagged_items = TaggedItem.objects.filter(tag=tag)
                        for tagged_item in tagged_items:
                            if TaggedItem.objects.filter(
                                tag=new_tag,
                                content_type=tagged_item.content_type,
                                object_id=tagged_item.object_id,
                            ).exists():
                                # we have the new tag as well, so we can just
                                # remove the tag association
                                tagged_item.delete()
                            else:
                                # point this taggedItem to the new one
                                tagged_item.tag = new_tag
                                tagged_item.save()

                self.message_user(request, "Tags have been merged", level="success")
                # clear the selected_tag_ids from session after merge is complete
                request.session.pop("selected_tag_ids", None)

                return redirect("..")
            else:
                self.message_user(request, "Form is invalid.", level="error")

        context = {
            "form": MergeTagsForm(),
            "selected_tag_ids": selected_tag_ids,
        }
        return render(request, "admin/taggit/merge_tags_form.html", context)
