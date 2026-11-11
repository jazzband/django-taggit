from django import forms
from django.test import TestCase
from django.test.utils import override_settings

from taggit.forms import TagField
from taggit.models import Tag


def _test_parse_tags(tagstring):
    if "," in tagstring:
        return tagstring.split(",")
    else:
        raise ValueError()


@override_settings(TAGGIT_TAGS_FROM_STRING="tests.test_forms._test_parse_tags")
class TagFieldTests(TestCase):
    def test_should_return_error_on_clean_if_not_comma_separated(self):
        class TestForm(forms.Form):
            tag = TagField()

        excpected_error = "Please provide a comma-separated list of tags."

        form = TestForm({"tag": "not-comma-separated"})

        self.assertFalse(form.is_valid())
        self.assertIn(excpected_error, form.errors["tag"])

    def test_should_always_return_False_on_has_change_if_disabled(self):
        class TestForm(forms.Form):
            tag = TagField(disabled=True)

        form = TestForm(initial={"tag": "foo,bar"}, data={"tag": ["a,b,c"]})

        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_changed())

    def test_should_return_True_if_form_has_changed(self):
        class TestForm(forms.Form):
            tag = TagField()

        form = TestForm(initial={"tag": [Tag(name="a")]}, data={"tag": ["b"]})

        self.assertTrue(form.has_changed())

    def test_should_return_False_if_form_has_not_changed(self):
        class TestForm(forms.Form):
            tag = TagField()

        form = TestForm(
            initial={"tag": [Tag(name="foo-bar")]}, data={"tag": ["foo-bar"]}
        )

        self.assertFalse(form.has_changed())

    def test_should_return_False_if_not_provided(self):
        class TestForm(forms.Form):
            tag = TagField()

        form = TestForm()

        self.assertFalse(form.has_changed())


class TagFieldMaxLengthTests(TestCase):
    def test_should_return_error_on_clean_if_tag_exceeds_max_length(self):
        class TestForm(forms.Form):
            tag = TagField()

        max_length = Tag._meta.get_field("name").max_length
        too_long_tag = "x" * (max_length + 1)

        form = TestForm({"tag": too_long_tag})

        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Tag(s) {too_long_tag} are over {max_length} characters",
            form.errors["tag"],
        )

    def test_should_be_valid_for_normal_length_tags(self):
        class TestForm(forms.Form):
            tag = TagField()

        max_length = Tag._meta.get_field("name").max_length
        ok_tag = "x" * max_length

        form = TestForm({"tag": ok_tag})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["tag"], [ok_tag])
