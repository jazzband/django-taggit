from django.contrib import admin
from django import forms
from django.db import transaction
from taggit.models import Tag, TaggedItem

from django.shortcuts import render, redirect
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
    actions = ["merge_tags"]

    def merge_tags(self, request, queryset):
        print("🚀 merge_tags called")
        print(f"Request method: ✅ {queryset}")
        print(f"Request POST data: 😊{request.POST}")

        if request.method == "POST" and "csrfmiddlewaretoken" in request.POST:
            form = MergeTagsForm(request.POST)
            if request.method == "POST":
                print("✅", "after form submission")
                new_tag_name = "fruit"  # hard coded value of the new tag
                new_tag, created = Tag.objects.get_or_create(name=new_tag_name)
                with transaction.atomic():
                    for tag in queryset:
                        for tagged_item in tag.taggit_taggeditem_items.all():
                            tagged_item.tag = new_tag
                            tagged_item.save()
                        # tag.delete()  #we can uncomment this to also remove the selected tags

                self.message_user(request, "Tags merged successfully.")
                return redirect(request.get_full_path())
            else:
                print(f"Form errors: {form.errors}")
                self.message_user(request, "Form is invalid.", level="error")
        else:
            form = MergeTagsForm()

        context = {
            "title": "Merge selected tags into a new tag",
            "form": form,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "queryset": queryset,
        }

        return render(
            request,
            "admin/taggit/merge_tags_form.html",
            context,
        )

    merge_tags.short_description = "Merge selected tags"
