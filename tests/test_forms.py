import random
import string

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

    def test_should_raise_error_on_clean_if_has_tag_longer_than_max_allowed(self):
        class TestForm(forms.Form):
            tag = TagField(max_tag_length=50)

        test_tag = "".join(random.choice(string.ascii_letters) for i in range(51))

        msg = "Tag(s) %(value_too_long)s are over %(max_tag_length)d characters" % {
            "value_too_long": test_tag,
            "max_tag_length": 50,
        }

        form = TestForm({"tag": test_tag})

        self.assertFalse(form.is_valid())
        self.assertIn(msg, form.errors["tag"])

        class TestForm(forms.Form):
            tag = TagField(max_tag_length=200)

        test_tag = "".join(random.choice(string.ascii_letters) for i in range(201))

        msg = "Tag(s) %(value_too_long)s are over %(max_tag_length)d characters" % {
            "value_too_long": test_tag,
            "max_tag_length": 200,
        }

        form = TestForm({"tag": test_tag})
        self.assertFalse(form.is_valid())
        self.assertIn(msg, form.errors["tag"])

        # Defaults to 100
        class TestForm(forms.Form):
            tag = TagField()

        test_tag = "".join(random.choice(string.ascii_letters) for i in range(101))

        msg = "Tag(s) %(value_too_long)s are over %(max_tag_length)d characters" % {
            "value_too_long": test_tag,
            "max_tag_length": 100,
        }

        form = TestForm({"tag": test_tag})
        self.assertFalse(form.is_valid())
        self.assertIn(msg, form.errors["tag"])

        # If None passed, uses Tag.name.field.max_length (which is 100)
        class TestForm(forms.Form):
            tag = TagField(max_tag_length=None)

        test_tag = "".join(random.choice(string.ascii_letters) for i in range(101))

        msg = "Tag(s) %(value_too_long)s are over %(max_tag_length)d characters" % {
            "value_too_long": test_tag,
            "max_tag_length": 100,
        }

        form = TestForm({"tag": test_tag})
        self.assertFalse(form.is_valid())
        self.assertIn(msg, form.errors["tag"])
