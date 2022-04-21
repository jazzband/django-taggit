from django.test import TestCase, override_settings

from tests.models import TestModel


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
