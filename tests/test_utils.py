import os
import os.path
from pathlib import Path

from django.test import TestCase
from django.utils import translation
from django.utils.translation.trans_real import all_locale_paths

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

    def test_po_files_up_to_date(self):
        locale_dir = self.get_locale_dir()
        for locale in os.listdir(locale_dir):
            # confirm there are files for each locale
            po_path = os.path.join(locale_dir, locale, "LC_MESSAGES", "django.po")
            if not os.path.exists(po_path):
                raise AssertionError(f"Missing .po file for the {locale} locale")
            mo_path = os.path.join(locale_dir, locale, "LC_MESSAGES", "django.mo")
            if not os.path.exists(mo_path):
                raise AssertionError(f"missing .mo file for the {locale} locale")

            if Path(po_path).stat().st_mtime > Path(mo_path).stat().st_mtime:
                raise AssertionError(
                    f"{po_path} is newer than {mo_path}, did you forget to run compilemessages?"
                )

    def test_language_file_integrity(self):
        locale_dir = self.get_locale_dir()
        for locale in os.listdir(locale_dir):
            # attempt translation activation to confirm that the language files are working
            with translation.override(locale):
                pass
