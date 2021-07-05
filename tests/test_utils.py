import os
import os.path

from django.test import TestCase
from django.utils import translation

from taggit.utils import split_strip


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
