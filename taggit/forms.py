from __future__ import unicode_literals

from django import forms
from django.utils import six
from django.utils.translation import ugettext as _

from taggit.models import Tag
from taggit.utils import edit_string_for_tags, parse_tags


class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags([
                o.tag for o in value.select_related("tag")])
        return super(TagWidget, self).render(name, value, attrs)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)

        try:
            tags = parse_tags(value)
            max_length = Tag._meta.get_field('name').max_length

            for tag in tags:
                if len(tag) > max_length:
                    raise forms.ValidationError(_("Tag '{0}' is longer than the {1} character limit.".format(tag, max_length)))

            return tags

        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags."))
