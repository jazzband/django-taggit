from django.test import TestCase

from taggit.models import Tag
from taggit.services.tag_merging import TagMergingService
from tests.models import DirectFood, Food, HousePet


class TagMergingServiceTests(TestCase):
    def setUp(self):
        self.service = TagMergingService()
        self.tag0 = Tag.objects.create(name="PyThon")
        self.tag1 = Tag.objects.create(name="Python")
        self.tag2 = Tag.objects.create(name="python")
        self.tag3 = Tag.objects.create(name="Django")
        self.tag4 = Tag.objects.create(name="PythonFundamentals")

    def test_merging_identical_tags_does_nothing(self):
        def filter_same_tag(tag, base_tag_name):
            return tag.objects.filter(name=base_tag_name)

        self.service.merge_tags(self.tag1.name, filter_same_tag)
        self.assertEqual(Tag.objects.count(), 5)

    def test_merging_case_insensitive_tags_merges_correctly(self):
        self.service.merge_case_insensitive_tags("python")
        self.assertEqual(Tag.objects.count(), 3)
        self.assertFalse(Tag.objects.filter(name="Python").exists())
        self.assertTrue(Tag.objects.filter(name="python").exists())

    def test_merging_tags_with_itself_does_not_delete_it(self):
        def filter_python(tag, base_tag_name):
            return tag.objects.filter(name=base_tag_name)

        self.service.merge_tags(self.tag1.name, filter_python)
        self.assertTrue(Tag.objects.filter(name="Python").exists())

    def test_merging_tags_deletes_duplicates(self):
        def filter_starts_with(tag, _):
            return tag.objects.filter(name__istartswith="python")

        self.service.merge_tags(self.tag1.name, filter_starts_with)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertFalse(Tag.objects.filter(name="PythonFundamentals").exists())
        self.assertTrue(Tag.objects.filter(name="Python").exists())

    def test_merging_tags_updates_tagged_items_correctly(self):
        # Create instances of DirectFood and DirectPet
        food_item = Food.objects.create(name="Apple")
        pet_item = HousePet.objects.create(name="Fido")

        # Tag the instances
        food_item.tags.add(self.tag0)
        pet_item.tags.add(self.tag1)

        self.service.merge_case_insensitive_tags("python")

        # Refresh the instances from the database
        food_item.refresh_from_db()
        pet_item.refresh_from_db()

        # Assert that the tags have been updated to the merged tag
        self.assertTrue(food_item.tags.filter(name="python").exists())
        self.assertTrue(pet_item.tags.filter(name="python").exists())

    def test_merging_tags_direct_updates_tagged_items_correctly(self):
        # Create instances of DirectFood and DirectPet
        food_item = DirectFood.objects.create(name="Apple")

        # Tag the instances
        food_item.tags.add(self.tag0)
        food_item.tags.add(self.tag1)

        # Merge the tags
        service = TagMergingService()
        service.merge_case_insensitive_tags("python")

        # Refresh the instances from the database
        food_item.refresh_from_db()

        # Assert that the tags have been updated to the merged tag
        self.assertTrue(food_item.tags.filter(name="python").exists())
