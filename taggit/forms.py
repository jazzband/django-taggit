from __future__ import unicode_literals

from django import forms
from django.utils import six
from django.forms import widgets
from taggit.utils import parse_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string


class TagWidget(widgets.Widget):
    """
    A widget that allows users to easily input tags in an interface
    powered by jQuery Tag-It (https://github.com/aehlke/tag-it)
    """
    def __init__(self, *args, **kwargs):
        """
        On initialization of the widget, the developer can set
        `placeholder_text` to override the language used in the new
        tag input box.
        """
        self.placeholder_text = kwargs.pop('placeholder_text', _('Add tag'))
        super(TagWidget, self).__init__(*args, **kwargs)

    def _media(self):
        """
        The JS files required are jQueryUI (Django's jQuery is assumed to
        already be present), jQuery Tag-It and an initialization file
        specifically for Django-Taggit.
        """
        js = (
            'taggit/js/jquery-ui.js',
            'taggit/js/tag-it.js',
            'taggit/js/django-taggit.js',
        )
        """
        The CSS files required are jQuery Tag-It, a flavor of ui-zendesk for
        barebones jQuery UI styles, and custom styles for Django-Taggit to
        bring the widget closer to Django's default admin.
        """
        css = {
            'all': (
                'taggit/css/jquery.tagit.css',
                'taggit/css/tagit.ui-zendesk.css',
                'taggit/css/django-taggit.css'
            )
        }
        return forms.Media(css=css, js=js)
    media = property(_media)

    def render(self, name, value, attrs=None):
        """
        Renders the widget HTML, placing the widgets in alphabetical order.
        """
        # Alphabetize the tag list
        tags = sorted(value.select_related("tag"), key=lambda x: x.tag.name)
        # Render the HTML
        output = render_to_string('taggit/widget.html', {
            'widget_name': name,
            'tag_list': tags,
            'placeholder_text': self.placeholder_text
        })
        # Return the safe HTML
        return mark_safe(output)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(
                _("Please provide a comma-separated list of tags."))
