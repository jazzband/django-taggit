from django.test import TestCase

from taggit.models import Tag
from taggit.tests.forms import FoodForm
from taggit.tests.models import Food

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
        
        pair = Food.objects.create(name="pair")
        pair.tags.add('green')
        self.assert_tags_equal(pair.tags.all(), ['green'])
        self.assert_tags_equal(Food.tags.all(), ['green'])
        
        apple.tags.add('red')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red'])
        self.assert_tags_equal(Food.tags.all(), ['green', 'red'])
        
        self.assert_tags_equal(Food.tags.most_common(), ['green', 'red'])
        
        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(Food.tags.all(), ['green', 'red'])

class TaggableFormTestCase(BaseTaggingTest):
    def test_form(self):
        self.assertEqual(FoodForm.base_fields.keys(), ['name', 'tags'])
        
        f = FoodForm({'name': 'apple', 'tags': 'green, red, yummy'})
        f.save()
        
        apple = Food.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])
