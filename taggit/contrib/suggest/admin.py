from django.contrib import admin

from taggit.admin import TaggedItemInline
from taggit.contrib.suggest.models import TagKeyword, TagRegex
from taggit.models import Tag


class TagKeywordInline(admin.StackedInline):
    model = TagKeyword


class TagRegxInline(admin.StackedInline):
    model = TagRegex


class TagSuggestAdmin(admin.ModelAdmin):
    inlines = [
        TaggedItemInline,
        TagKeywordInline,
        TagRegxInline,
    ]


admin.site.unregister(Tag)
admin.site.register(Tag, TagSuggestAdmin)
