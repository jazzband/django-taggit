from django.test import TestCase

from taggit.models import Tag
from taggit.tests.forms import FoodForm
from taggit.tests.models import Food, Pet


class BaseTaggingTest(TestCase):
    def assert_tags_equal(self, qs, tags):
        tags = Tag.objects.filter(name__in=tags)
        self.assertEqual(list(qs), list(tags))


class AddTagTestCase(BaseTaggingTest):
    def test_add_tag(self):
        apple = Food.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(Food.tags.all()),  [])
        
        apple.tags.add('green')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(Food.tags.all(), ['green'])
        
        pear = Food.objects.create(name="pear")
        pear.tags.add('green')
        self.assert_tags_equal(pear.tags.all(), ['green'])
        self.assert_tags_equal(Food.tags.all(), ['green'])
        
        apple.tags.add('red')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red'])
        self.assert_tags_equal(Food.tags.all(), ['green', 'red'])
        
        self.assert_tags_equal(Food.tags.most_common(), ['green', 'red'])

        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(Food.tags.all(), ['green', 'red'])


class LookupByTagTestCase(BaseTaggingTest):
    def test_lookup_by_tag(self):
        apple = Food.objects.create(name="apple")
        apple.tags.add("red", "green")
        pear = Food.objects.create(name="pear")
        pear.tags.add("green")
        
        self.assertEqual(list(Food.objects.filter(tags__in=["red"])), [apple])
        self.assertEqual(list(Food.objects.filter(tags__in=["green"])), [apple, pear])
        
        kitty = Pet.objects.create(name="kitty")
        kitty.tags.add("fuzzy", "red")
        dog = Pet.objects.create(name="dog")
        dog.tags.add("woof", "red")
        self.assertEqual(list(Food.objects.filter(tags__in=["red"]).distinct()), [apple])


class TaggableFormTestCase(BaseTaggingTest):
    def test_form(self):
        self.assertEqual(FoodForm.base_fields.keys(), ['name', 'tags'])
        
        f = FoodForm({'name': 'apple', 'tags': 'green, red, yummy'})
        f.save()
        
        apple = Food.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])
