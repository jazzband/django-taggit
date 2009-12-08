from django import forms

from taggit.utils import parse_tags


class TagField(forms.CharField):
    def clean(self, value):
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError("Please provide a comma seperate list of tags.")
