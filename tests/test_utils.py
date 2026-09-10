import os
import os.path

from django.test import TestCase
from django.utils import translation

from taggit.utils import edit_string_for_tags, parse_tags, split_strip


class SplitStripTests(TestCase):
    def test_should_return_empty_list_if_not_string(self):
        result = split_strip(None)

        self.assertListEqual(result, [])

    def test_should_return_list_of_non_empty_words(self):
        expected_result = ["foo", "bar"]

        result = split_strip("foo|bar||", delimiter="|")

        self.assertListEqual(result, expected_result)


class TestLanguages(TestCase):
    maxDiff = None

    def get_locale_dir(self):
        return os.path.join(os.path.dirname(__file__), "..", "taggit", "locale")

    def test_language_file_integrity(self):
        locale_dir = self.get_locale_dir()
        for locale in os.listdir(locale_dir):
            # attempt translation activation to confirm that the language files are working
            with translation.override(locale):
                pass


class EditStringForTagsTests(TestCase):
    def test_with_tag_instances(self):
        class DummyTag:
            def __init__(self, name):
                self.name = name

        tags = [DummyTag("tag1"), DummyTag("tag with space"), DummyTag("tag,comma")]
        self.assertEqual(edit_string_for_tags(tags), '"tag with space", "tag,comma", tag1')

    def test_with_strings(self):
        tags = ["tag1", "tag with space", "tag,comma"]
        self.assertEqual(edit_string_for_tags(tags), '"tag with space", "tag,comma", tag1')

    def test_with_empty_list(self):
        self.assertEqual(edit_string_for_tags([]), "")


class ParseTagsTests(TestCase):
    def test_basic_parse(self):
        self.assertEqual(parse_tags("foo, bar, baz"), ["bar", "baz", "foo"])

    def test_quoted_tags(self):
        self.assertEqual(parse_tags('"foo bar", baz'), ["baz", "foo bar"])

    def test_empty_string(self):
        self.assertEqual(parse_tags(""), [])

