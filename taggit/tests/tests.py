from django.test import TestCase

from taggit.models import Tag
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
