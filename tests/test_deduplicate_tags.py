from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from taggit.models import Tag, TaggedItem
from tests.models import Food, HousePet


class DeduplicateTagsTests(TestCase):
    def setUp(self):
        settings.TAGGIT_CASE_INSENSITIVE = True

        self.tag1 = Tag.objects.create(name="Python")
        self.tag2 = Tag.objects.create(name="python")
        self.tag3 = Tag.objects.create(name="PYTHON")

        self.food_item = Food.objects.create(name="Apple")
        self.pet_item = HousePet.objects.create(name="Fido")

        self.food_item.tags.add(self.tag1)
        self.pet_item.tags.add(self.tag2)
        self.pet_item.tags.add(self.tag3)

    def test_deduplicate_tags(self):
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(TaggedItem.objects.count(), 3)

        out = StringIO()
        call_command("deduplicate_tags", stdout=out)

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(TaggedItem.objects.count(), 2)

        self.assertTrue(Tag.objects.filter(name__iexact="python").exists())
        self.assertEqual(
            TaggedItem.objects.filter(tag__name__iexact="python").count(), 2
        )

        self.assertIn("Tag deduplication complete.", out.getvalue())

    def test_no_duplicates(self):
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(TaggedItem.objects.count(), 3)

        out = StringIO()
        call_command("deduplicate_tags", stdout=out)

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(TaggedItem.objects.count(), 2)

        self.assertTrue(Tag.objects.filter(name__iexact="python").exists())
        self.assertEqual(
            TaggedItem.objects.filter(tag__name__iexact="python").count(), 2
        )

        self.assertIn("Tag deduplication complete.", out.getvalue())

    def test_taggit_case_insensitive_not_enabled(self):
        settings.TAGGIT_CASE_INSENSITIVE = False

        out = StringIO()
        call_command("deduplicate_tags", stdout=out)

        self.assertIn("TAGGIT_CASE_INSENSITIVE is not enabled.", out.getvalue())

        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(TaggedItem.objects.count(), 3)
