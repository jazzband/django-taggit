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

    def test_disabled_field_with_model_instances(self):
        class TestForm(forms.Form):
            tag = TagField(disabled=True)

        initial_tags = [Tag(name="apple"), Tag(name="banana")]
        form = TestForm(initial={"tag": initial_tags}, data={"tag": "other"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["tag"], initial_tags)

    def test_disabled_field_with_string_initial(self):
        class TestForm(forms.Form):
            tag = TagField(disabled=True)

        form = TestForm(initial={"tag": "apple,banana"}, data={"tag": "other"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["tag"], ["apple", "banana"])

    def test_disabled_field_with_none_initial(self):
        class TestForm(forms.Form):
            tag = TagField(disabled=True, required=False)

        form = TestForm(initial={"tag": None}, data={"tag": "other"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["tag"], [])

    def test_disabled_field_in_model_form(self):
        from .forms import FoodForm
        from .models import Food

        food = Food.objects.create(name="Apple")
        food.tags.add("red", "sweet")

        form = FoodForm(
            data={"name": "Green Apple", "tags": "green,sour"},
            instance=food,
        )
        form.fields["tags"].disabled = True

        self.assertTrue(form.is_valid())
        saved_food = form.save()
        self.assertEqual(saved_food.name, "Green Apple")
        self.assertSequenceEqual(
            saved_food.tags.order_by("name").values_list("name", flat=True),
            ["red", "sweet"],
        )
