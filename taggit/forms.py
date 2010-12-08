from django import forms
from django.utils.simplejson import dumps
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from taggit.models import Tag
from taggit.utils import parse_tags, edit_string_for_tags, LazyEncoder

class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
        output = super(TagWidget, self).render(name, value, attrs)
        tags = dumps([tag.name for tag in Tag.objects.all().order_by('name')], cls=LazyEncoder)
        
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery(document).ready(function() {
                tagsExisting = %s;
                jQuery("#id_%s").autocomplete(tagsExisting, {
                    width: 150,
                    max: 10,
                    min: 3,
                    highlight: false,
                    multiple: true,
                    multipleSeparator: ", ",
                    scroll: true,
                    scrollHeight: 300,
                    //matchContains: true,
                    autoFill: true,
                    selectFirst: false
                });
            });
            </script>''' % (tags, name))

class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))