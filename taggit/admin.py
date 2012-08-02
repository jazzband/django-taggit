from django.contrib import admin

from taggit.models import Tag, TaggedItem


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", 'slug')
    search_fields = ('name', 'slug')
    inlines = [
        TaggedItemInline
    ]


admin.site.register(Tag, TagAdmin)
