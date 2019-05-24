from django import forms
from django.db import models
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
        # Always return False if the field is disabled since self.bound_data
        # always uses the initial value in this case.
        if self.disabled:
            return False

        try:
            data_value = self.clean(data_value)
        except forms.ValidationError:
            pass

        if initial_value is None:
            initial_value = []

        initial_value = [tag.name for tag in initial_value]
        initial_value.sort()

        return initial_value != data_value


class TagMultipleChoiceField(forms.ModelMultipleChoiceField):
    def prepare_value(self, data):
        if isinstance(data, models.query.QuerySet):
            data = [o.tag for o in data.select_related('tag')]
        return super(TagMultipleChoiceField, self).prepare_value(data)
