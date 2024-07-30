from django.core.management import call_command
from django.test import TestCase

from taggit.models import Tag
from tests.models import Food, HousePet


class RemoveOrphanedTagsTests(TestCase):
    def setUp(self):
        # Create some tags, some orphaned and some not
        self.orphan_tag1 = Tag.objects.create(name="Orphan1")
        self.orphan_tag2 = Tag.objects.create(name="Orphan2")
        self.used_tag = Tag.objects.create(name="Used")

        # Create instances of Food and HousePet and tag them
        self.food_item = Food.objects.create(name="Apple")
        self.pet_item = HousePet.objects.create(name="Fido")

        self.food_item.tags.add(self.used_tag)
        self.pet_item.tags.add(self.used_tag)

    def test_remove_orphaned_tags(self):
        # Ensure the setup is correct
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.filter(taggit_taggeditem_items=None).count(), 2)

        # Call the management command to remove orphaned tags
        call_command("remove_orphaned_tags")

        # Check the count of tags after running the command
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.filter(taggit_taggeditem_items=None).count(), 0)

        # Ensure that the used tag still exists
        self.assertTrue(Tag.objects.filter(name="Used").exists())
        self.assertFalse(Tag.objects.filter(name="Orphan1").exists())
        self.assertFalse(Tag.objects.filter(name="Orphan2").exists())

    def test_no_orphaned_tags(self):
        # Ensure the setup is correct
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.filter(taggit_taggeditem_items=None).count(), 2)

        # Add used_tag to food_item to make no tags orphaned
        self.food_item.tags.add(self.orphan_tag1)
        self.food_item.tags.add(self.orphan_tag2)

        # Call the management command to remove orphaned tags
        call_command("remove_orphaned_tags")

        # Check the count of tags after running the command
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.filter(taggit_taggeditem_items=None).count(), 0)

        # Ensure all tags still exist
        self.assertTrue(Tag.objects.filter(name="Used").exists())
        self.assertTrue(Tag.objects.filter(name="Orphan1").exists())
        self.assertTrue(Tag.objects.filter(name="Orphan2").exists())
