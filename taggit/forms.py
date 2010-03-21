from django import forms

from taggit.utils import parse_tags


class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = ", ".join(o.tag.name for o in value.select_related("tag"))
        return super(TagWidget, self).render(name, value, attrs)

class TagField(forms.CharField):
    widget = TagWidget
    
    def clean(self, value):
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError("Please provide a comma seperate list of tags.")
