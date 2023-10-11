from django.test import TestCase, override_settings

from taggit.models import Tag
from tests.models import TestModel


class TestTaggableManager(TestCase):
    def test_set_ordering(self):
        """
        Test that the tags are set and returned exactly
        """
        str_tags = ["red", "green", "delicious"]
        sample_obj = TestModel.objects.create()

        sample_obj.tags.set(str_tags)
        for idx, tag in enumerate(sample_obj.tags.all()):
            self.assertEqual(tag.name, str_tags[idx])

    def test_set_mixed(self):
        """
        Test with mixed str and obj tags
        """
        tag_obj = Tag.objects.create(name="mcintosh")
        str_tags = ["red", "green", "delicious"]
        sample_obj = TestModel.objects.create()

        sample_obj.tags.set(str_tags + [tag_obj])
        results = str_tags + [tag_obj.name]
        for idx, tag in enumerate(sample_obj.tags.all()):
            self.assertEqual(tag.name, results[idx])


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

    def test_old_slugs(self):
        """
        Test that the setting that gives us the old slugification behavior
        is in place
        """
        with override_settings(TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING=True):
            sample_obj = TestModel.objects.create()
            # a unicode tag will be slugified for space reasons but
            # unicode-ness will be kept by default
            sample_obj.tags.add("あい うえお")
            self.assertEqual([tag.slug for tag in sample_obj.tags.all()], [""])


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
