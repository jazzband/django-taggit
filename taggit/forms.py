from django import forms

from taggit.utils import parse_tags


class TaggableForm(forms.ModelForm):
    tags = forms.CharField(help_text="A comma seperated list of tags.")
    
    def save(self, commit=True):
        obj = super(TaggableForm, self).save(commit=False)
        def save_tags():
            # TODO: Remove the assumption that the manager is named 'tags'
            obj.tags.set(parse_tags(self.cleaned_data['tags']))
        if commit:
            obj.save()
            save_tags()
        else:
            obj.save_tags = save_tags
        return obj
