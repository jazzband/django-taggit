from contextlib import contextmanager
from unittest import skipIf

from django.test import TestCase, override_settings

from taggit import models as taggit_models
from tests.models import TestModel


@contextmanager
def disable_unidecode():
    """
    Disable unidecode temporarily
    """
    old_installed_value = taggit_models.unidecode_installed
    taggit_models.unidecode_installed = False
    try:
        yield
    finally:
        taggit_models.unidecode_installed = old_installed_value


class TestTaggableManager(TestCase):
    def test_duplicates(self):
        sample_obj = TestModel.objects.create()
        sample_obj.tags.set(["green", "green"])
        desired_result = ["green"]
        self.assertEqual(desired_result, [tag.name for tag in sample_obj.tags.all()])


class TestSlugification(TestCase):
    def test_unicode_slugs(self):
        """
        Confirm the preservation of unicode in slugification by default
        """
        sample_obj = TestModel.objects.create()
        # a unicode tag will be slugified for space reasons but
        # unicode-ness will be kept by default
        sample_obj.tags.add("あい うえお")
        self.assertEqual([tag.slug for tag in sample_obj.tags.all()], ["あい-うえお"])

    def test_old_slugs_wo_unidecode(self):
        """
        Test that the setting that gives us the old slugification behavior
        is in place
        """
        with (
            disable_unidecode(),
            override_settings(TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING=True),
        ):
            sample_obj = TestModel.objects.create()
            sample_obj.tags.add("aあい うえおb")
            # when unidecode is not installed, the unicode ends up being passed directly
            # to slugify, and will get "wiped"
            self.assertEqual([tag.slug for tag in sample_obj.tags.all()], ["a-b"])

    @skipIf(
        not taggit_models.unidecode_installed,
        "This test requires unidecode to be installed",
    )
    def test_old_slugs_with_unidecode(self):
        """
        Test that the setting that gives us the old slugification behavior
        is in place
        """
        with override_settings(TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING=True):
            sample_obj = TestModel.objects.create()
            # unidecode will transform the tag on top of slugification
            sample_obj.tags.add("あい うえお")
            self.assertEqual([tag.slug for tag in sample_obj.tags.all()], ["ai-ueo"])


class TestPrefetchCache(TestCase):
    def setUp(self) -> None:
        sample_obj = TestModel.objects.create()
        sample_obj.tags.set(["1", "2", "3"])

    def test_cache_clears_on_add(self):
        """
        Test that the prefetch cache gets cleared on tag addition
        """
        sample_obj = TestModel.objects.prefetch_related("tags").get()
        self.assertTrue(sample_obj.tags.is_cached(sample_obj))

        sample_obj.tags.add("4")
        self.assertFalse(sample_obj.tags.is_cached(sample_obj))

    def test_cache_clears_on_remove(self):
        """
        Test that the prefetch cache gets cleared on tag removal
        """
        sample_obj = TestModel.objects.prefetch_related("tags").get()
        self.assertTrue(sample_obj.tags.is_cached(sample_obj))

        sample_obj.tags.remove("3")
        self.assertFalse(sample_obj.tags.is_cached(sample_obj))

    def test_cache_clears_on_clear(self):
        """
        Test that the prefetch cache gets cleared when tags are cleared
        """
        sample_obj = TestModel.objects.prefetch_related("tags").get()
        self.assertTrue(sample_obj.tags.is_cached(sample_obj))

        sample_obj.tags.clear()
        self.assertFalse(sample_obj.tags.is_cached(sample_obj))
