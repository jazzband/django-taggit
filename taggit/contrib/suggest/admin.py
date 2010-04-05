from django.contrib import admin 

from taggit.models import Tag 
from taggit.admin import TaggedItemInline 
from taggit.contrib.suggest.models import TagKeyword, TagRegExp

class TagKeywordInline(admin.StackedInline):
    model = TagKeyword 

class TagRegExpInline(admin.StackedInline): 
    model = TagRegExp

class TagSuggestAdmin(admin.ModelAdmin): 
    inlines = [
            TaggedItemInline,
            TagKeywordInline,
            TagRegExpInline,
            ]

admin.site.unregister(Tag) 
admin.site.register(Tag, TagSuggestAdmin)
