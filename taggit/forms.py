from __future__ import unicode_literals

from django import forms
from django.utils import six
from django.utils.inspect import func_supports_parameter
from django.utils.translation import ugettext as _

from taggit.utils import edit_string_for_tags, parse_tags


class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags([
                o.tag for o in value.select_related("tag")])
        kwargs = {}
        if func_supports_parameter(super(TagWidget, self).render, 'renderer'):
            # Django >= 1.11 supports the renderer argument.
            kwargs['renderer'] = renderer
        return super(TagWidget, self).render(name, value, attrs, **kwargs)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags."))
