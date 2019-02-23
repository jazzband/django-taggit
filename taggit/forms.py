from django import forms
from django.utils.translation import gettext as _

from taggit.utils import edit_string_for_tags, parse_tags


class TagWidget(forms.TextInput):
    def format_value(self, value):
        if value is not None and not isinstance(value, str):
            value = edit_string_for_tags(value)
        return super().format_value(value)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super().clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags.")
            )

    def has_changed(self, initial_value, data_value):
        initial_value = [tag.name for tag in initial_value]
        initial_value.sort()
        try:
            data_value = self.clean(data_value)
        except forms.ValidationError:
            pass
        return initial_value != data_value
