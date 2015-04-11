from __future__ import absolute_import, unicode_literals

from unittest import TestCase as UnitTestCase

import django
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import TestCase, TransactionTestCase
from django.utils.encoding import force_text

from .forms import CustomPKFoodForm, DirectFoodForm, FoodForm, OfficialFoodForm
from .models import (Article, Child, CustomManager, CustomPKFood,
                     CustomPKHousePet, CustomPKPet, DirectFood,
                     DirectHousePet, DirectPet, Food, HousePet, Movie,
                     OfficialFood, OfficialHousePet, OfficialPet,
                     OfficialTag, OfficialThroughModel, Pet, Photo,
                     TaggedCustomPKFood, TaggedCustomPKPet, TaggedFood,
                     TaggedPet)

from taggit.managers import _model_name, _TaggableManager, TaggableManager
from taggit.models import Tag, TaggedItem

from taggit.utils import edit_string_for_tags, parse_tags

try:
    from unittest import skipIf, skipUnless
except ImportError:
    from django.utils.unittest import skipIf, skipUnless


class BaseTaggingTest(object):
    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
        got = [getattr(obj, attr) for obj in qs]
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)

    def _get_form_str(self, form_str):
        if django.VERSION >= (1, 3):
            form_str %= {
                "help_start": '<span class="helptext">',
                "help_stop": "</span>"
            }
        else:
            form_str %= {
                "help_start": "",
                "help_stop": ""
            }
        return form_str

    def assert_form_renders(self, form, html):
        self.assertHTMLEqual(str(form), self._get_form_str(html))


class BaseTaggingTestCase(TestCase, BaseTaggingTest):
    pass


class BaseTaggingTransactionTestCase(TransactionTestCase, BaseTaggingTest):
    pass


class TagModelTestCase(BaseTaggingTransactionTestCase):
    food_model = Food
    tag_model = Tag

    def test_unique_slug(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("Red", "red")

    def test_update(self):
        special = self.tag_model.objects.create(name="special")
        special.save()

    def test_add(self):
        apple = self.food_model.objects.create(name="apple")
        yummy = self.tag_model.objects.create(name="yummy")
        apple.tags.add(yummy)

    def test_slugify(self):
        a = Article.objects.create(title="django-taggit 1.0 Released")
        a.tags.add("awesome", "release", "AWESOME")
        self.assert_tags_equal(a.tags.all(), [
            "category-awesome",
            "category-release",
            "category-awesome-1"
        ], attr="slug")

    def test_integers(self):
        """Adding an integer as a tag should raise a ValueError (#237)."""
        apple = self.food_model.objects.create(name="apple")
        with self.assertRaisesRegexp(ValueError, (
                r"Cannot add 1 \(<(type|class) 'int'>\). "
                r"Expected <class 'django.db.models.base.ModelBase'> or str.")):
            apple.tags.add(1)

class TagModelDirectTestCase(TagModelTestCase):
    food_model = DirectFood
    tag_model = Tag

class TagModelCustomPKTestCase(TagModelTestCase):
    food_model = CustomPKFood
    tag_model = Tag

class TagModelOfficialTestCase(TagModelTestCase):
    food_model = OfficialFood
    tag_model = OfficialTag

class TaggableManagerTestCase(BaseTaggingTestCase):
    food_model = Food
    pet_model = Pet
    housepet_model = HousePet
    taggeditem_model = TaggedItem
    tag_model = Tag

    def test_add_tag(self):
        apple = self.food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(self.food_model.tags.all()), [])

        apple.tags.add('green')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add('green')
        self.assert_tags_equal(pear.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        apple.tags.add('red')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])

        self.assert_tags_equal(
            self.food_model.tags.most_common(),
            ['green', 'red'],
            sort=False
        )

        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])
        tag = self.tag_model.objects.create(name="delicious")
        apple.tags.add(tag)
        self.assert_tags_equal(apple.tags.all(), ["red", "delicious"])

        apple.delete()
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])

    def test_add_queries(self):
        # Prefill content type cache:
        ContentType.objects.get_for_model(self.food_model)
        apple = self.food_model.objects.create(name="apple")
        #   1  query to see which tags exist
        # + 3  queries to create the tags.
        # + 6  queries to create the intermediary things (including SELECTs, to
        #      make sure we don't double create.
        # + 12 on Django 1.6 for save points.
        queries = 22
        if django.VERSION < (1, 6):
            queries -= 12
        self.assertNumQueries(queries, apple.tags.add, "red", "delicious", "green")

        pear = self.food_model.objects.create(name="pear")
        #   1 query to see which tags exist
        # + 4 queries to create the intermeidary things (including SELECTs, to
        #     make sure we dont't double create.
        # + 4 on Django 1.6 for save points.
        queries = 9
        if django.VERSION < (1, 6):
            queries -= 4
        self.assertNumQueries(queries, pear.tags.add, "green", "delicious")

        self.assertNumQueries(0, pear.tags.add)

    def test_require_pk(self):
        food_instance = self.food_model()
        self.assertRaises(ValueError, lambda: food_instance.tags.all())

    def test_delete_obj(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red")
        self.assert_tags_equal(apple.tags.all(), ["red"])
        strawberry = self.food_model.objects.create(name="strawberry")
        strawberry.tags.add("red")
        apple.delete()
        self.assert_tags_equal(strawberry.tags.all(), ["red"])

    def test_delete_bulk(self):
        apple = self.food_model.objects.create(name="apple")
        kitty = self.pet_model.objects.create(pk=apple.pk, name="kitty")

        apple.tags.add("red", "delicious", "fruit")
        kitty.tags.add("feline")

        self.food_model.objects.all().delete()

        self.assert_tags_equal(kitty.tags.all(), ["feline"])

    def test_lookup_by_tag(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green")
        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green")
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["red"])),
            [apple]
        )
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["green"])),
            [apple, pear]
        )

        kitty = self.pet_model.objects.create(name="kitty")
        kitty.tags.add("fuzzy", "red")
        dog = self.pet_model.objects.create(name="dog")
        dog.tags.add("woof", "red")
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["red"]).distinct()),
            [apple]
        )

        tag = self.tag_model.objects.get(name="woof")
        self.assertEqual(list(self.pet_model.objects.filter(tags__in=[tag])), [dog])

        cat = self.housepet_model.objects.create(name="cat", trained=True)
        cat.tags.add("fuzzy")

        pks = self.pet_model.objects.filter(tags__name__in=["fuzzy"])
        model_name = self.pet_model.__name__
        self.assertQuerysetEqual(pks,
                                 ['<{0}: kitty>'.format(model_name),
                                  '<{0}: cat>'.format(model_name)],
                                 ordered=False)

    def test_lookup_bulk(self):
        apple = self.food_model.objects.create(name="apple")
        pear = self.food_model.objects.create(name="pear")
        apple.tags.add('fruit', 'green')
        pear.tags.add('fruit', 'yummie')

        def lookup_qs():
            # New fix: directly allow WHERE object_id IN (SELECT id FROM ..)
            objects = self.food_model.objects.all()
            lookup = self.taggeditem_model.bulk_lookup_kwargs(objects)
            list(self.taggeditem_model.objects.filter(**lookup))

        def lookup_list():
            # Simulate old situation: iterate over a list.
            objects = list(self.food_model.objects.all())
            lookup = self.taggeditem_model.bulk_lookup_kwargs(objects)
            list(self.taggeditem_model.objects.filter(**lookup))

        self.assertNumQueries(1, lookup_qs)
        self.assertNumQueries(2, lookup_list)

    def test_exclude(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green", "delicious")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "delicious")

        self.food_model.objects.create(name="guava")

        pks = self.food_model.objects.exclude(tags__name__in=["red"])
        model_name = self.food_model.__name__
        self.assertQuerysetEqual(pks,
                                 ['<{0}: pear>'.format(model_name),
                                  '<{0}: guava>'.format(model_name)],
                                 ordered=False)

    def test_similarity_by_tag(self):
        """Test that pears are more similar to apples than watermelons"""
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green", "juicy", "small", "sour")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "juicy", "small", "sweet")

        watermelon = self.food_model.objects.create(name="watermelon")
        watermelon.tags.add("green", "juicy", "large", "sweet")

        similar_objs = apple.tags.similar_objects()
        self.assertEqual(similar_objs, [pear, watermelon])
        self.assertEqual([obj.similar_tags for obj in similar_objs],
                         [3, 2])

    def test_tag_reuse(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy", "juicy")
        self.assert_tags_equal(apple.tags.all(), ['juicy'])

    def test_query_traverse(self):
        spot = self.pet_model.objects.create(name='Spot')
        spike = self.pet_model.objects.create(name='Spike')
        spot.tags.add('scary')
        spike.tags.add('fluffy')
        lookup_kwargs = {
            '%s__name' % _model_name(self.pet_model): 'Spot'
        }
        self.assert_tags_equal(
            self.tag_model.objects.filter(**lookup_kwargs),
            ['scary']
        )

    def test_taggeditem_unicode(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy")

        self.assertEqual(
            force_text(self.taggeditem_model.objects.all()[0]),
            "apple tagged with juicy"
        )

    def test_abstract_subclasses(self):
        p = Photo.objects.create()
        p.tags.add("outdoors", "pretty")
        self.assert_tags_equal(
            p.tags.all(),
            ["outdoors", "pretty"]
        )

        m = Movie.objects.create()
        m.tags.add("hd")
        self.assert_tags_equal(
            m.tags.all(),
            ["hd"],
        )

    def test_field_api(self):
        # Check if tag field, which simulates m2m, has django-like api.
        field = self.food_model._meta.get_field('tags')
        self.assertTrue(hasattr(field, 'rel'))
        self.assertTrue(hasattr(field.rel, 'to'))
        self.assertTrue(hasattr(field, 'related'))

        # This API has changed in Django 1.8
        # https://code.djangoproject.com/ticket/21414
        if django.VERSION >= (1, 8):
            self.assertEqual(self.food_model, field.model)
            self.assertEqual(self.tag_model, field.related.model)
        else:
            self.assertEqual(self.food_model, field.related.model)

    def test_names_method(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add('green')
        apple.tags.add('red')
        self.assertEqual(list(apple.tags.names()), ['green', 'red'])

    def test_slugs_method(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add('green and juicy')
        apple.tags.add('red')
        self.assertEqual(list(apple.tags.slugs()), ['green-and-juicy', 'red'])

    def test_serializes(self):
        apple = self.food_model.objects.create(name="apple")
        serializers.serialize("json", (apple,))

    def test_prefetch_related(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add('1', '2')
        orange = self.food_model.objects.create(name="orange")
        orange.tags.add('2', '4')
        with self.assertNumQueries(2):
            l = list(self.food_model.objects.prefetch_related('tags').all())
        with self.assertNumQueries(0):
            foods = dict((f.name, set(t.name for t in f.tags.all())) for f in l)
            self.assertEqual(foods, {
                'orange': set(['2', '4']),
                'apple': set(['1', '2'])
            })

    def test_internal_type_is_manytomany(self):
        self.assertEqual(
            TaggableManager().get_internal_type(), 'ManyToManyField'
        )

class TaggableManagerDirectTestCase(TaggableManagerTestCase):
    food_model = DirectFood
    pet_model = DirectPet
    housepet_model = DirectHousePet
    taggeditem_model = TaggedFood

class TaggableManagerCustomPKTestCase(TaggableManagerTestCase):
    food_model = CustomPKFood
    pet_model = CustomPKPet
    housepet_model = CustomPKHousePet
    taggeditem_model = TaggedCustomPKFood

    def test_require_pk(self):
        # TODO with a charfield pk, pk is never None, so taggit has no way to
        # tell if the instance is saved or not
        pass

class TaggableManagerOfficialTestCase(TaggableManagerTestCase):
    food_model = OfficialFood
    pet_model = OfficialPet
    housepet_model = OfficialHousePet
    taggeditem_model = OfficialThroughModel
    tag_model = OfficialTag

    def test_extra_fields(self):
        self.tag_model.objects.create(name="red")
        self.tag_model.objects.create(name="delicious", official=True)
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("delicious", "red")

        pear = self.food_model.objects.create(name="Pear")
        pear.tags.add("delicious")

        self.assertEqual(apple, self.food_model.objects.get(tags__official=False))

class TaggableManagerInitializationTestCase(TaggableManagerTestCase):
    """Make sure manager override defaults and sets correctly."""
    food_model = Food
    custom_manager_model = CustomManager

    def test_default_manager(self):
        self.assertEqual(self.food_model.tags.__class__, _TaggableManager)

    def test_custom_manager(self):
        self.assertEqual(self.custom_manager_model.tags.__class__, CustomManager.Foo)

class TaggableFormTestCase(BaseTaggingTestCase):
    form_class = FoodForm
    food_model = Food

    def test_form(self):
        self.assertEqual(list(self.form_class.base_fields), ['name', 'tags'])

        f = self.form_class({'name': 'apple', 'tags': 'green, red, yummy'})
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy" id="id_tags" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])

        f = self.form_class({'name': 'apple', 'tags': 'green, red, yummy, delicious'}, instance=apple)
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy', 'delicious'])
        self.assertEqual(self.food_model.objects.count(), 1)

        f = self.form_class({"name": "raspberry"})
        self.assertFalse(f.is_valid())

        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="delicious, green, red, yummy" id="id_tags" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

        apple.tags.add('has,comma')
        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="&quot;has,comma&quot;, delicious, green, red, yummy" id="id_tags" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

        apple.tags.add('has space')
        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="&quot;has space&quot;, &quot;has,comma&quot;, delicious, green, red, yummy" id="id_tags" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

    def test_formfield(self):
        tm = TaggableManager(verbose_name='categories', help_text='Add some categories', blank=True)
        ff = tm.formfield()
        self.assertEqual(ff.label, 'Categories')
        self.assertEqual(ff.help_text, 'Add some categories')
        self.assertEqual(ff.required, False)

        self.assertEqual(ff.clean(""), [])

        tm = TaggableManager()
        ff = tm.formfield()
        self.assertRaises(ValidationError, ff.clean, "")

class TaggableFormDirectTestCase(TaggableFormTestCase):
    form_class = DirectFoodForm
    food_model = DirectFood

class TaggableFormCustomPKTestCase(TaggableFormTestCase):
    form_class = CustomPKFoodForm
    food_model = CustomPKFood

class TaggableFormOfficialTestCase(TaggableFormTestCase):
    form_class = OfficialFoodForm
    food_model = OfficialFood


class TagStringParseTestCase(UnitTestCase):
    """
    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """

    def test_with_simple_space_delimited_tags(self):
        """
        Test with simple space-delimited tags.
        """
        self.assertEqual(parse_tags('one'), ['one'])
        self.assertEqual(parse_tags('one two'), ['one', 'two'])
        self.assertEqual(parse_tags('one two three'), ['one', 'three', 'two'])
        self.assertEqual(parse_tags('one one two two'), ['one', 'two'])

    def test_with_comma_delimited_multiple_words(self):
        """
        Test with comma-delimited multiple words.
        An unquoted comma in the input will trigger this.
        """
        self.assertEqual(parse_tags(',one'), ['one'])
        self.assertEqual(parse_tags(',one two'), ['one two'])
        self.assertEqual(parse_tags(',one two three'), ['one two three'])
        self.assertEqual(parse_tags('a-one, a-two and a-three'),
                         ['a-one', 'a-two and a-three'])

    def test_with_double_quoted_multiple_words(self):
        """
        Test with double-quoted multiple words.
        A completed quote will trigger this.  Unclosed quotes are ignored.
        """
        self.assertEqual(parse_tags('"one'), ['one'])
        self.assertEqual(parse_tags('"one two'), ['one', 'two'])
        self.assertEqual(parse_tags('"one two three'), ['one', 'three', 'two'])
        self.assertEqual(parse_tags('"one two"'), ['one two'])
        self.assertEqual(parse_tags('a-one "a-two and a-three"'),
                         ['a-one', 'a-two and a-three'])

    def test_with_no_loose_commas(self):
        """
        Test with no loose commas -- split on spaces.
        """
        self.assertEqual(parse_tags('one two "thr,ee"'), ['one', 'thr,ee', 'two'])

    def test_with_loose_commas(self):
        """
        Loose commas - split on commas
        """
        self.assertEqual(parse_tags('"one", two three'), ['one', 'two three'])

    def test_tags_with_double_quotes_can_contain_commas(self):
        """
        Double quotes can contain commas
        """
        self.assertEqual(parse_tags('a-one "a-two, and a-three"'),
                         ['a-one', 'a-two, and a-three'])
        self.assertEqual(parse_tags('"two", one, one, two, "one"'),
                         ['one', 'two'])

    def test_with_naughty_input(self):
        """
        Test with naughty input.
        """
        # Bad users! Naughty users!
        self.assertEqual(parse_tags(None), [])
        self.assertEqual(parse_tags(''), [])
        self.assertEqual(parse_tags('"'), [])
        self.assertEqual(parse_tags('""'), [])
        self.assertEqual(parse_tags('"' * 7), [])
        self.assertEqual(parse_tags(',,,,,,'), [])
        self.assertEqual(parse_tags('",",",",",",","'), [','])
        self.assertEqual(parse_tags('a-one "a-two" and "a-three'),
                         ['a-one', 'a-three', 'a-two', 'and'])

    def test_recreation_of_tag_list_string_representations(self):
        plain = Tag.objects.create(name='plain')
        spaces = Tag.objects.create(name='spa ces')
        comma = Tag.objects.create(name='com,ma')
        self.assertEqual(edit_string_for_tags([plain]), 'plain')
        self.assertEqual(edit_string_for_tags([plain, spaces]), '"spa ces", plain')
        self.assertEqual(edit_string_for_tags([plain, spaces, comma]), '"com,ma", "spa ces", plain')
        self.assertEqual(edit_string_for_tags([plain, comma]), '"com,ma", plain')
        self.assertEqual(edit_string_for_tags([comma, spaces]), '"com,ma", "spa ces"')


@skipIf(django.VERSION < (1, 7), "not relevant for Django < 1.7")
class DeconstructTestCase(UnitTestCase):
    def test_deconstruct_kwargs_kept(self):
        instance = TaggableManager(through=OfficialThroughModel, to='dummy.To')
        name, path, args, kwargs = instance.deconstruct()
        new_instance = TaggableManager(*args, **kwargs)
        self.assertEqual('tests.OfficialThroughModel', new_instance.rel.through)
        self.assertEqual('dummy.To', new_instance.rel.to)


@skipUnless(django.VERSION < (1, 7), "test only applies to 1.6 and below")
class SouthSupportTests(TestCase):
    def test_import_migrations_module(self):
        try:
            from taggit.migrations import __doc__  # noqa
        except ImproperlyConfigured as e:
            exception = e
        self.assertIn("SOUTH_MIGRATION_MODULES", exception.args[0])


class InheritedPrefetchTests(TestCase):

    def test_inherited_tags_with_prefetch(self):
        child = Child()
        child.save()
        child.tags.add('tag 1', 'tag 2', 'tag 3', 'tag 4')

        child = Child.objects.get()
        no_prefetch_tags = child.tags.all()
        self.assertEquals(4, no_prefetch_tags.count())
        child = Child.objects.prefetch_related('tags').get()
        prefetch_tags = child.tags.all()
        self.assertEquals(4, prefetch_tags.count())
        self.assertEquals(set([t.name for t in no_prefetch_tags]),
                          set([t.name for t in prefetch_tags]))
