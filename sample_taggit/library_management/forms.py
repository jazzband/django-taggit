# Path: `library_management/forms.py`
from django import forms

from taggit.forms import TagWidget
from taggit.models import Tag

from .models import Author, Book, ConditionTag, PhysicalCopy


class PhysicalCopyForm(forms.ModelForm):
    condition_tags = forms.ModelMultipleChoiceField(
        queryset=ConditionTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PhysicalCopy
        fields = ["condition_tags"]


class AuthorForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "birth_date",
            "biography",
            "tags",
        ]


class BookForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Book
        fields = ["name", "author", "published_date", "isbn", "summary", "tags"]
