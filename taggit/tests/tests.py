from __future__ import with_statement
from contextlib import contextmanager

from django.test import TestCase

from taggit.models import Tag
from taggit.tests.forms import FoodForm
from taggit.tests.models import Food, Pet, HousePet


class BaseTaggingTest(TestCase):
    def assert_tags_equal(self, qs, tags, sort=True):
        got = map(lambda tag: tag.name, qs)
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)
    
    @contextmanager
    def assert_raises(self, exc_type):
        try:
            yield
        except Exception, e:
            self.assert_(type(e) is exc_type, "%s didn't match expected "
                "exception type %s" % (e, exc_type))
        else:
            self.fail("No exception raised, expected %s" % exc_type)
    

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

        self.assert_tags_equal(Food.tags.most_common(), ['green', 'red'], sort=False)

        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(Food.tags.all(), ['green', 'red'])
        tag = Tag.objects.create(name="delicious")
        apple.tags.add(tag)
        self.assert_tags_equal(apple.tags.all(), ["red", "delicious"])
        
        apple.delete()
        self.assert_tags_equal(Food.tags.all(), ["green"])
        
        f = Food()
        with self.assert_raises(ValueError):
            f.tags.all()
    
    def test_unique_slug(self):
        apple = Food.objects.create(name="apple")
        apple.tags.add("Red", "red")


class DeleteObjecTestCase(BaseTaggingTest):
    def test_delete_obj(self):
        apple = Food.objects.create(name="apple")
        apple.tags.add("red")
        self.assert_tags_equal(apple.tags.all(), ["red"])
        strawberry = Food.objects.create(name="strawberry")
        strawberry.tags.add("red")
        apple.delete()
        self.assert_tags_equal(strawberry.tags.all(), ["red"])


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

        tag = Tag.objects.get(name="woof")
        self.assertEqual(list(Pet.objects.filter(tags__in=[tag])), [dog])

        cat = HousePet.objects.create(name="cat", trained=True)
        cat.tags.add("fuzzy")

        self.assertEqual(
            map(lambda o: o.pk, Pet.objects.filter(tags__in=["fuzzy"])),
            [kitty.pk, cat.pk]
        )


class TaggableFormTestCase(BaseTaggingTest):
    def test_form(self):
        self.assertEqual(FoodForm.base_fields.keys(), ['name', 'tags'])

        f = FoodForm({'name': 'apple', 'tags': 'green, red, yummy'})
        self.assertEqual(str(f), """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>\n<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy" id="id_tags" /></td></tr>""")
        f.save()
        apple = Food.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])

        f = FoodForm({'name': 'apple', 'tags': 'green, red, yummy, delicious'}, instance=apple)
        f.save()
        apple = Food.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy', 'delicious'])
        self.assertEqual(Food.objects.count(), 1)
        
        f = FoodForm({"name": "raspberry"})
        raspberry = f.save()
        self.assert_tags_equal(raspberry.tags.all(), [])
        
        f = FoodForm(instance=apple)
        self.assertEqual(str(f), """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>\n<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy, delicious" id="id_tags" /></td></tr>""")


class SimilarityByTagTestCase(BaseTaggingTest):
    def test_similarity_by_tag(self):
        """Test that pears are more similar to apples than watermelons"""
        apple = Food.objects.create(name="apple")
        apple.tags.add("green", "juicy", "small", "sour")

        pear = Food.objects.create(name="pear")
        pear.tags.add("green", "juicy", "small", "sweet")

        watermelon = Food.objects.create(name="watermelon")
        watermelon.tags.add("green", "juicy", "large", "sweet")

        similar_objs = apple.tags.similar_objects()
        self.assertEqual(similar_objs, [pear, watermelon])
        self.assertEqual(map(lambda x: x.similar_tags, similar_objs), [3, 2])


class TagReuseTestCase(BaseTaggingTest):
    def test_tag_reuse(self):
        apple = Food.objects.create(name="apple")
        apple.tags.add("juicy", "juicy")
        self.assert_tags_equal(apple.tags.all(), ['juicy'])
