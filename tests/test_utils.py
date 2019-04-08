from django.test import TestCase

from taggit.utils import split_strip


class SplitStripTests(TestCase):
    def test_should_return_empty_list_if_not_string(self):
        result = split_strip(None)

        self.assertListEqual(result, [])

    def test_should_return_list_of_non_empty_words(self):
        expected_result = ["foo", "bar"]

        result = split_strip("foo|bar||", delimiter="|")

        self.assertListEqual(result, expected_result)
