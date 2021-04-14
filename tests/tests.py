from unittest import mock

from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, models
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.test.utils import override_settings

from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import Tag, TaggedItem
from taggit.utils import edit_string_for_tags, parse_tags
from taggit.views import tagged_object_list

from .forms import (
    BlankTagForm,
    CustomPKFoodForm,
    DirectCustomPKFoodForm,
    DirectFoodForm,
    FoodForm,
    OfficialFoodForm,
)
from .models import (
    Article,
    Child,
    CustomManager,
    CustomPKFood,
    CustomPKHousePet,
    CustomPKPet,
    DirectCustomPKFood,
    DirectCustomPKHousePet,
    DirectCustomPKPet,
    DirectFood,
    DirectHousePet,
    DirectPet,
    DirectTrackedFood,
    DirectTrackedHousePet,
    DirectTrackedPet,
    Food,
    HousePet,
    Movie,
    MultiInheritanceFood,
    Name,
    OfficialFood,
    OfficialHousePet,
    OfficialPet,
    OfficialTag,
    OfficialThroughModel,
    Pet,
    Photo,
    ProxyPhoto,
    TaggedCustomPK,
    TaggedCustomPKFood,
    TaggedFood,
    TaggedTrackedFood,
    TrackedTag,
    UUIDFood,
    UUIDHousePet,
    UUIDPet,
    UUIDTag,
    UUIDTaggedItem,
)


class BaseTaggingTestCase(TestCase):
    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
        got = [getattr(obj, attr) for obj in qs]
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)


class TagModelTestCase(BaseTaggingTestCase):
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
        self.assert_tags_equal(
            a.tags.all(),
            ["category-awesome", "category-release", "category-awesome-1"],
            attr="slug",
        )

    def test_integers(self):
        """Adding an integer as a tag should raise a ValueError (#237)."""
        apple = self.food_model.objects.create(name="apple")
        with self.assertRaisesRegex(
            ValueError,
            (
                r"Cannot add 1 \(<(type|class) 'int'>\). "
                r"Expected <class 'django.db.models.base.ModelBase'> or str."
            ),
        ):
            apple.tags.add(1)

    def test_gt(self):
        high = self.tag_model.objects.create(name="high")
        low = self.tag_model.objects.create(name="Low")
        self.assertIs(low > high, True)
        self.assertIs(high > low, False)

    def test_lt(self):
        high = self.tag_model.objects.create(name="high")
        low = self.tag_model.objects.create(name="Low")
        self.assertIs(high < low, True)
        self.assertIs(low < high, False)


class CustomTagCreationTestCase(TestCase):
    def test_model_manager_add(self):
        apple = OfficialFood.objects.create(name="apple")

        # let's add two official tags
        apple.tags.add("foo", "bar", tag_kwargs={"official": True})

        # and two unofficial ones
        apple.tags.add("baz", "wow", tag_kwargs={"official": False})

        # We should end up with 4 tags
        self.assertEquals(apple.tags.count(), 4)
        self.assertEquals(apple.tags.filter(official=True).count(), 2)
        self.assertEquals(apple.tags.filter(official=False).count(), 2)


class TagModelDirectTestCase(TagModelTestCase):
    food_model = DirectFood
    tag_model = Tag


class TagModelDirectCustomPKTestCase(TagModelTestCase):
    food_model = DirectCustomPKFood
    tag_model = Tag


class TagModelCustomPKTestCase(TagModelTestCase):
    food_model = CustomPKFood
    tag_model = Tag


class TagModelOfficialTestCase(TagModelTestCase):
    food_model = OfficialFood
    tag_model = OfficialTag


class TagUUIDModelTestCase(TagModelTestCase):
    food_model = UUIDFood
    tag_model = UUIDTag


class TaggableManagerTestCase(BaseTaggingTestCase):
    food_model = Food
    multi_inheritance_food_model = MultiInheritanceFood
    pet_model = Pet
    housepet_model = HousePet
    taggeditem_model = TaggedItem
    tag_model = Tag

    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()

    def test_add_tag(self):
        apple = self.food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(self.food_model.tags.all()), [])

        apple.tags.add("green")
        self.assert_tags_equal(apple.tags.all(), ["green"])
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green")
        self.assert_tags_equal(pear.tags.all(), ["green"])
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])

        apple.tags.add("red")
        self.assert_tags_equal(apple.tags.all(), ["green", "red"])
        self.assert_tags_equal(self.food_model.tags.all(), ["green", "red"])

        self.assert_tags_equal(
            self.food_model.tags.most_common(), ["green", "red"], sort=False
        )

        self.assert_tags_equal(
            self.food_model.tags.most_common(min_count=2), ["green"], sort=False
        )

        apple.tags.remove("green")
        self.assert_tags_equal(apple.tags.all(), ["red"])
        self.assert_tags_equal(self.food_model.tags.all(), ["green", "red"])
        tag = self.tag_model.objects.create(name="delicious")
        apple.tags.add(tag)
        self.assert_tags_equal(apple.tags.all(), ["red", "delicious"])

        apple.delete()
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_add_new_tag_sends_m2m_changed_signals(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green")
        green_pk = self.tag_model.objects.get(name="green").pk

        self.assertEqual(send_mock.call_count, 2)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_add_existing_tag_sends_m2m_changed_signals(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        green = self.tag_model.objects.create(name="green")
        apple.tags.add("green")

        self.assertEqual(send_mock.call_count, 2)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green.pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green.pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_add_second_tag_sends_m2m_changed_signals_with_correct_new_pks(
        self, send_mock
    ):
        apple = self.food_model.objects.create(name="apple")
        green = self.tag_model.objects.create(name="green")
        apple.tags.add("red")
        send_mock.reset_mock()
        apple.tags.add("green", "red")

        self.assertEqual(send_mock.call_count, 2)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green.pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green.pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_remove_tag_sends_m2m_changed_signals(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green")
        green_pk = self.tag_model.objects.get(name="green").pk
        send_mock.reset_mock()

        apple.tags.remove("green")

        self.assertEqual(send_mock.call_count, 2)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_remove",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_remove",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_clear_sends_m2m_changed_signal(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red")
        send_mock.reset_mock()
        apple.tags.clear()

        self.assertEqual(send_mock.call_count, 2)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_clear",
                    instance=apple,
                    model=self.tag_model,
                    pk_set=None,
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_clear",
                    instance=apple,
                    model=self.tag_model,
                    pk_set=None,
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_set_with_clear_true_sends_m2m_changed_signal(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green")
        apple.tags.add("red")
        send_mock.reset_mock()

        apple.tags.set("red", clear=True)

        red_pk = self.tag_model.objects.get(name="red").pk

        self.assertEqual(send_mock.call_count, 4)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_clear",
                    instance=apple,
                    model=self.tag_model,
                    pk_set=None,
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_clear",
                    instance=apple,
                    model=self.tag_model,
                    pk_set=None,
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="pre_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={red_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={red_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    @mock.patch("django.db.models.signals.m2m_changed.send")
    def test_set_sends_m2m_changed_signal(self, send_mock):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green")
        send_mock.reset_mock()

        apple.tags.set("red")

        green_pk = self.tag_model.objects.get(name="green").pk
        red_pk = self.tag_model.objects.get(name="red").pk

        self.assertEqual(send_mock.call_count, 4)
        send_mock.assert_has_calls(
            [
                mock.call(
                    action="pre_remove",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_remove",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={green_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="pre_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={red_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
                mock.call(
                    action="post_add",
                    instance=apple,
                    model=self.tag_model,
                    pk_set={red_pk},
                    reverse=False,
                    sender=self.taggeditem_model,
                    using="default",
                ),
            ]
        )

    def test_add_queries(self):
        # Prefill content type cache:
        ContentType.objects.get_for_model(self.food_model)
        apple = self.food_model.objects.create(name="apple")
        # 1. SELECT "taggit_tag"."id", "taggit_tag"."name", "taggit_tag"."slug" FROM "taggit_tag" WHERE "taggit_tag"."name" IN ('green', 'red', 'delicious')
        # 2. SELECT "taggit_tag"."id", "taggit_tag"."name", "taggit_tag"."slug" FROM "taggit_tag" WHERE "taggit_tag"."name" = 'green'
        # 3. SAVEPOINT
        # 4. SAVEPOINT
        # 5. INSERT INTO "taggit_tag" ("name", "slug") VALUES ('green', 'green')
        # 6. RELEASE SAVEPOINT
        # 7. RELEASE SAVEPOINT
        # 8. SELECT "taggit_tag"."id", "taggit_tag"."name", "taggit_tag"."slug" FROM "taggit_tag" WHERE "taggit_tag"."name" = 'red'
        # 9. SAVEPOINT
        # 10. SAVEPOINT
        # 11. INSERT INTO "taggit_tag" ("name", "slug") VALUES ('red', 'red')
        # 12. RELEASE SAVEPOINT
        # 13. RELEASE SAVEPOINT
        # 14. SELECT "taggit_tag"."id", "taggit_tag"."name", "taggit_tag"."slug" FROM "taggit_tag" WHERE "taggit_tag"."name" = 'delicious'
        # 15. SAVEPOINT
        # 16. SAVEPOINT
        # 17. INSERT INTO "taggit_tag" ("name", "slug") VALUES ('delicious', 'delicious')
        # 18. RELEASE SAVEPOINT
        # 19. RELEASE SAVEPOINT
        # 20. SELECT "taggit_taggeditem"."tag_id" FROM "taggit_taggeditem" WHERE ("taggit_taggeditem"."content_type_id" = 20 AND "taggit_taggeditem"."object_id" = 1)
        # 21. SELECT "taggit_taggeditem"."id", "taggit_taggeditem"."tag_id", "taggit_taggeditem"."content_type_id", "taggit_taggeditem"."object_id" FROM "taggit_taggeditem" WHERE ("taggit_taggeditem"."content_type_id" = 20 AND "taggit_taggeditem"."object_id" = 1 AND "taggit_taggeditem"."tag_id" = 1)
        # 22. SAVEPOINT
        # 23. INSERT INTO "taggit_taggeditem" ("tag_id", "content_type_id", "object_id") VALUES (1, 20, 1)
        # 24. RELEASE SAVEPOINT
        # 25. SELECT "taggit_taggeditem"."id", "taggit_taggeditem"."tag_id", "taggit_taggeditem"."content_type_id", "taggit_taggeditem"."object_id" FROM "taggit_taggeditem" WHERE ("taggit_taggeditem"."content_type_id" = 20 AND "taggit_taggeditem"."object_id" = 1 AND "taggit_taggeditem"."tag_id" = 2)
        # 26. SAVEPOINT
        # 27. INSERT INTO "taggit_taggeditem" ("tag_id", "content_type_id", "object_id") VALUES (2, 20, 1)
        # 28. RELEASE SAVEPOINT
        # 29. SELECT "taggit_taggeditem"."id", "taggit_taggeditem"."tag_id", "taggit_taggeditem"."content_type_id", "taggit_taggeditem"."object_id" FROM "taggit_taggeditem" WHERE ("taggit_taggeditem"."content_type_id" = 20 AND "taggit_taggeditem"."object_id" = 1 AND "taggit_taggeditem"."tag_id" = 3)
        # 30. SAVEPOINT
        # 31. INSERT INTO "taggit_taggeditem" ("tag_id", "content_type_id", "object_id") VALUES (3, 20, 1)
        # 32. RELEASE SAVEPOINT
        queries = 32
        self.assertNumQueries(queries, apple.tags.add, "red", "delicious", "green")

        pear = self.food_model.objects.create(name="pear")
        #   1 query to see which tags exist
        #   1  query to check existing ids for sending m2m_changed signal
        # + 4 queries to create the intermeidary things (including SELECTs, to
        #     make sure we dont't double create.
        # + 4 for save points.
        queries = 10
        self.assertNumQueries(queries, pear.tags.add, "green", "delicious")

        #   1  query to check existing ids for sending m2m_changed signal
        self.assertNumQueries(1, pear.tags.add)

    def test_require_pk(self):
        food_instance = self.food_model()
        msg = (
            "%s objects need to have a primary key value before you can access "
            "their tags." % type(self.food_model()).__name__
        )
        with self.assertRaisesMessage(ValueError, msg):
            food_instance.tags.all()

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
            list(self.food_model.objects.filter(tags__name__in=["red"])), [apple]
        )
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["green"])),
            [apple, pear],
        )

        kitty = self.pet_model.objects.create(name="kitty")
        kitty.tags.add("fuzzy", "red")
        dog = self.pet_model.objects.create(name="dog")
        dog.tags.add("woof", "red")
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["red"]).distinct()),
            [apple],
        )

        tag = self.tag_model.objects.get(name="woof")
        self.assertEqual(list(self.pet_model.objects.filter(tags__in=[tag])), [dog])

        cat = self.housepet_model.objects.create(name="cat", trained=True)
        cat.tags.add("fuzzy")

        pks = self.pet_model.objects.filter(tags__name__in=["fuzzy"])
        model_name = self.pet_model.__name__
        self.assertQuerysetEqual(
            pks,
            ["<{}: kitty>".format(model_name), "<{}: cat>".format(model_name)],
            ordered=False,
        )

    def test_exclude(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green", "delicious")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "delicious")

        self.food_model.objects.create(name="guava")

        pks = self.food_model.objects.exclude(tags__name__in=["red"])
        model_name = self.food_model.__name__
        self.assertQuerysetEqual(
            pks,
            ["<{}: pear>".format(model_name), "<{}: guava>".format(model_name)],
            ordered=False,
        )

    def test_multi_inheritance_similarity_by_tag(self):
        """Test that pears are more similar to apples than watermelons using multi_inheritance"""
        apple = self.multi_inheritance_food_model.objects.create(name="apple")
        apple.tags.add("green", "juicy", "small", "sour")

        pear = self.multi_inheritance_food_model.objects.create(name="pear")
        pear.tags.add("green", "juicy", "small", "sweet")

        watermelon = self.multi_inheritance_food_model.objects.create(name="watermelon")
        watermelon.tags.add("green", "juicy", "large", "sweet")

        similar_objs = apple.tags.similar_objects()
        self.assertEqual(similar_objs, [pear, watermelon])
        self.assertEqual([obj.similar_tags for obj in similar_objs], [3, 2])

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
        self.assertEqual([obj.similar_tags for obj in similar_objs], [3, 2])

    def test_tag_reuse(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy", "juicy")
        self.assert_tags_equal(apple.tags.all(), ["juicy"])

    def test_query_traverse(self):
        spot = self.pet_model.objects.create(name="Spot")
        spike = self.pet_model.objects.create(name="Spike")
        spot.tags.add("scary")
        spike.tags.add("fluffy")
        lookup_kwargs = {"%s__name" % self.pet_model._meta.model_name: "Spot"}
        self.assert_tags_equal(
            self.tag_model.objects.filter(**lookup_kwargs), ["scary"]
        )

    def test_taggeditem_str(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy")

        self.assertEqual(
            str(self.taggeditem_model.objects.first()), "apple tagged with juicy"
        )

    def test_taggeditem_through_defaults(self):
        if self.taggeditem_model != OfficialThroughModel:
            self.skipTest(
                "Through default tests are only run when the tagged item model has extra_field"
            )
        apple = self.food_model.objects.create(name="kiwi")
        apple.tags.add("juicy", through_defaults={"extra_field": "green"})

        self.assertEqual(
            str(self.taggeditem_model.objects.first()), "kiwi tagged with juicy"
        )
        self.assertEqual(self.taggeditem_model.objects.first().extra_field, "green")

    def test_abstract_subclasses(self):
        p = Photo.objects.create()
        p.tags.add("outdoors", "pretty")
        self.assert_tags_equal(p.tags.all(), ["outdoors", "pretty"])

        m = Movie.objects.create()
        m.tags.add("hd")
        self.assert_tags_equal(m.tags.all(), ["hd"])

    def test_proxy_subclasses(self):
        p = Photo.objects.create()
        proxy_p = ProxyPhoto.objects.create()
        p.tags.add("outdoors", "pretty")
        self.assert_tags_equal(p.tags.all(), ["outdoors", "pretty"])
        self.assert_tags_equal(proxy_p.tags.all(), [])

        proxy_p.tags.add("hd")
        self.assert_tags_equal(proxy_p.tags.all(), ["hd"])
        self.assert_tags_equal(p.tags.all(), ["outdoors", "pretty"])

    def test_field_api(self):
        # Check if tag field, which simulates m2m, has django-like api.
        field = self.food_model._meta.get_field("tags")
        self.assertTrue(hasattr(field, "remote_field"))
        self.assertTrue(hasattr(field.remote_field, "model"))
        self.assertEqual(self.food_model, field.model)
        self.assertEqual(self.tag_model, field.remote_field.model)

    def test_names_method(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green")
        apple.tags.add("red")
        self.assertEqual(sorted(list(apple.tags.names())), ["green", "red"])

    def test_slugs_method(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green and juicy")
        apple.tags.add("red")
        self.assertEqual(sorted(list(apple.tags.slugs())), ["green-and-juicy", "red"])

    def test_serializes(self):
        apple = self.food_model.objects.create(name="apple")
        serializers.serialize("json", (apple,))

    def test_prefetch_related(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("1", "2")
        orange = self.food_model.objects.create(name="orange")
        orange.tags.add("2", "4")
        with self.assertNumQueries(2):
            list_prefetched = list(
                self.food_model.objects.prefetch_related("tags").all()
            )
        with self.assertNumQueries(0):
            foods = {f.name: {t.name for t in f.tags.all()} for f in list_prefetched}
            self.assertEqual(foods, {"orange": {"2", "4"}, "apple": {"1", "2"}})

    def test_internal_type_is_manytomany(self):
        self.assertEqual(TaggableManager().get_internal_type(), "ManyToManyField")

    def test_prefetch_no_extra_join(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("1", "2")
        with self.assertNumQueries(2):
            list(self.food_model.objects.prefetch_related("tags").all())
            join_clause = 'INNER JOIN "%s"' % self.taggeditem_model._meta.db_table
            self.assertEqual(
                connection.queries[-1]["sql"].count(join_clause),
                1,
                connection.queries[-2:],
            )

    @override_settings(TAGGIT_CASE_INSENSITIVE=True)
    def test_with_case_insensitive_option(self):
        spain = self.tag_model.objects.create(name="Spain", slug="spain")
        orange = self.food_model.objects.create(name="orange")
        orange.tags.add("spain")
        self.assertEqual(list(orange.tags.all()), [spain])

    @override_settings(TAGGIT_CASE_INSENSITIVE=True)
    def test_with_case_insensitive_option_and_creation(self):
        orange = self.food_model.objects.create(name="orange")
        orange.tags.add("spain", "Spain")
        tag_names = list(orange.tags.names())
        self.assertEqual(len(tag_names), 1, tag_names)

    @override_settings(TAGGIT_CASE_INSENSITIVE=True)
    def test_with_case_insensitive_option_new_and_old(self):
        orange = self.food_model.objects.create(name="orange")
        orange.tags.add("Spain")
        tag_names = list(orange.tags.names())
        self.assertEqual(len(tag_names), 1, tag_names)
        orange.tags.add("spain", "Valencia")
        tag_names = sorted(orange.tags.names())
        self.assertEqual(tag_names, ["Spain", "Valencia"])

    def test_tag_uniqueness(self):
        apple = self.food_model.objects.create(name="apple")
        tag = self.tag_model.objects.create(name="juice", slug="juicy")
        self.taggeditem_model.objects.create(tag=tag, content_object=apple)
        with self.assertRaises(IntegrityError):
            self.taggeditem_model.objects.create(tag=tag, content_object=apple)

    def test_most_common_lazy(self):
        with self.assertNumQueries(0):
            qs = self.food_model.tags.most_common()
        with self.assertNumQueries(1):
            list(qs)


class TaggableManagerDirectTestCase(TaggableManagerTestCase):
    food_model = DirectFood
    pet_model = DirectPet
    housepet_model = DirectHousePet
    taggeditem_model = TaggedFood


class TaggableManagerDirectTrackedTestCase(TaggableManagerTestCase):
    food_model = DirectTrackedFood
    pet_model = DirectTrackedPet
    housepet_model = DirectTrackedHousePet
    taggeditem_model = TaggedTrackedFood
    tag_model = TrackedTag


class TaggableManagerDirectCustomPKTestCase(TaggableManagerTestCase):
    food_model = DirectCustomPKFood
    pet_model = DirectCustomPKPet
    housepet_model = DirectCustomPKHousePet
    taggeditem_model = TaggedCustomPKFood

    def test_require_pk(self):
        # With a CharField pk, pk is never None. So taggit has no way to tell
        # if the instance is saved or not.
        pass


class TaggableManagerCustomPKTestCase(TaggableManagerTestCase):
    food_model = CustomPKFood
    pet_model = CustomPKPet
    housepet_model = CustomPKHousePet
    taggeditem_model = TaggedCustomPK

    def test_require_pk(self):
        # With a CharField pk, pk is never None. So taggit has no way to tell
        # if the instance is saved or not.
        pass


class TaggableManagerUUIDTestCase(TaggableManagerTestCase):
    food_model = UUIDFood
    pet_model = UUIDPet
    housepet_model = UUIDHousePet
    taggeditem_model = UUIDTaggedItem
    tag_model = UUIDTag

    def test_require_pk(self):
        # With a UUIDField pk, pk is never None. So taggit has no way to tell
        # if the instance is saved or not.
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

    def test_get_tags_with_count(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green", "delicious")
        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "delicious")

        tag_info = self.tag_model.objects.filter(
            officialfood__in=[apple.id, pear.id], name="green"
        ).annotate(models.Count("name"))
        self.assertEqual(tag_info[0].name__count, 2)

    def test_most_common_extra_filters(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red")
        apple.tags.add("green")

        orange = self.food_model.objects.create(name="orange")
        orange.tags.add("orange")
        orange.tags.add("red")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green")
        pear.tags.add("yellow")

        self.assert_tags_equal(
            self.food_model.tags.most_common(
                min_count=2, extra_filters={"officialfood__name__in": ["pear", "apple"]}
            )[:1],
            ["green"],
            sort=False,
        )

        self.assert_tags_equal(
            self.food_model.tags.most_common(
                min_count=2,
                extra_filters={"officialfood__name__in": ["orange", "apple"]},
            )[:1],
            ["red"],
            sort=False,
        )


class TaggableManagerInitializationTestCase(TaggableManagerTestCase):
    """Make sure manager override defaults and sets correctly."""

    food_model = Food
    custom_manager_model = CustomManager

    def test_default_manager(self):
        self.assertIs(type(self.food_model.tags), _TaggableManager)

    def test_custom_manager(self):
        self.assertIs(type(self.custom_manager_model.tags), CustomManager.Foo)


class TaggableFormTestCase(BaseTaggingTestCase):
    form_class = FoodForm
    food_model = Food

    def _get_form_str(self, form_str):
        form_str %= {
            "help_start": '<span class="helptext">',
            "help_stop": "</span>",
            "required": "required",
        }
        return form_str

    def assertFormRenders(self, form, html):
        self.assertHTMLEqual(str(form), self._get_form_str(html))

    def test_form(self):
        self.assertEqual(list(self.form_class.base_fields), ["name", "tags"])

        f = self.form_class({"name": "apple", "tags": "green, red, yummy"})
        self.assertFormRenders(
            f,
            """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" %(required)s /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy" id="id_tags" %(required)s /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""",
        )
        f.save()
        apple = self.food_model.objects.get(name="apple")
        self.assert_tags_equal(apple.tags.all(), ["green", "red", "yummy"])

        f = self.form_class(
            {"name": "apple", "tags": "green, red, yummy, delicious"}, instance=apple
        )
        f.save()
        apple = self.food_model.objects.get(name="apple")
        self.assert_tags_equal(apple.tags.all(), ["green", "red", "yummy", "delicious"])
        self.assertEqual(self.food_model.objects.count(), 1)

        f = self.form_class({"name": "raspberry"})
        self.assertFalse(f.is_valid())

        f = self.form_class(instance=apple)
        self.assertFormRenders(
            f,
            """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" %(required)s /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="delicious, green, red, yummy" id="id_tags" %(required)s /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""",
        )

        apple.tags.add("has,comma")
        f = self.form_class(instance=apple)
        self.assertFormRenders(
            f,
            """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" %(required)s /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="&quot;has,comma&quot;, delicious, green, red, yummy" id="id_tags" %(required)s /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""",
        )

        apple.tags.add("has space")
        f = self.form_class(instance=apple)
        self.assertFormRenders(
            f,
            """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" %(required)s /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="&quot;has space&quot;, &quot;has,comma&quot;, delicious, green, red, yummy" id="id_tags" %(required)s /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""",
        )

    def test_formfield(self):
        tm = TaggableManager(
            verbose_name="categories", help_text="Add some categories", blank=True
        )
        ff = tm.formfield()
        self.assertEqual(ff.label, "Categories")
        self.assertEqual(ff.help_text, "Add some categories")
        self.assertEqual(ff.required, False)

        self.assertEqual(ff.clean(""), [])

        tm = TaggableManager()
        ff = tm.formfield()
        self.assertRaises(ValidationError, ff.clean, "")

    def test_form_changed_data(self):
        # new food, blank tag
        pear = self.food_model()
        request = {"name": "pear", "tags": ""}
        fff = self.form_class(request, instance=pear)
        self.assertFalse(fff.is_valid())

        pear = self.food_model()
        request = {"name": "pear", "tags": "sweat"}
        fff = self.form_class(request, instance=pear)
        self.assertTrue(fff.is_valid())
        self.assertIn("tags", fff.changed_data)
        self.assertIn("name", fff.changed_data)
        fff.save()

        request = {"name": "pear", "tags": "yellow"}
        fff = self.form_class(request, instance=pear)
        self.assertTrue(fff.is_valid())
        self.assertIn("tags", fff.changed_data)
        self.assertNotIn("name", fff.changed_data)
        fff.save()

        # same object nothing changed
        fff = self.form_class(request, instance=pear)
        self.assertTrue(fff.is_valid())
        self.assertFalse(fff.changed_data)

        # delete tag
        request = {"name": "pear", "tags": ""}
        fff = self.form_class(request, instance=pear)
        self.assertFalse(fff.is_valid())  # tag not blank

        # change name, tags are the same
        request = {"name": "apple", "tags": "yellow"}
        fff = self.form_class(request, instance=pear)
        self.assertTrue(fff.is_valid())
        self.assertIn("name", fff.changed_data)
        self.assertNotIn("tags", fff.changed_data)
        fff.save()

        # tags changed
        apple = self.food_model.objects.get(name="apple")
        request = {"name": "apple", "tags": "yellow, delicious"}
        fff = self.form_class(request, instance=apple)
        self.assertTrue(fff.is_valid())
        self.assertNotIn("name", fff.changed_data)
        self.assertIn("tags", fff.changed_data)
        fff.save()

        # only tags order changed
        apple = self.food_model.objects.get(name="apple")
        request = {"name": "apple", "tags": "delicious, yellow"}
        fff = self.form_class(request, instance=apple)
        self.assertTrue(fff.is_valid())
        self.assertFalse(fff.changed_data)

        # and nothing changed
        fff = self.form_class(request, instance=apple)
        self.assertTrue(fff.is_valid())
        self.assertFalse(fff.changed_data)


class TaggableFormDirectTestCase(TaggableFormTestCase):
    form_class = DirectFoodForm
    food_model = DirectFood


class TaggableFormDirectCustomPKTestCase(TaggableFormTestCase):
    form_class = DirectCustomPKFoodForm
    food_model = DirectCustomPKFood


class TaggableFormCustomPKTestCase(TaggableFormTestCase):
    form_class = CustomPKFoodForm
    food_model = CustomPKFood


class TaggableFormOfficialTestCase(TaggableFormTestCase):
    form_class = OfficialFoodForm
    food_model = OfficialFood


class BlankFormTestCase(SimpleTestCase):
    form_class = BlankTagForm

    def test_early_access_to_changed_data_with(self):
        # For example in ModelForm.validate_unique().
        request = {"name": "pear"}
        form = self.form_class(request)
        self.assertNotIn("tags", form.changed_data)

        request = {"name": "pear", "tags": ""}
        form = self.form_class(request)
        self.assertNotIn("tags", form.changed_data)

        request = {"name": "pear", "tags": "tag1"}
        form = self.form_class(request)
        self.assertIn("tags", form.changed_data)


class TagStringParseTestCase(SimpleTestCase):
    """
    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """

    def test_with_simple_space_delimited_tags(self):
        """
        Test with simple space-delimited tags.
        """
        self.assertEqual(parse_tags("one"), ["one"])
        self.assertEqual(parse_tags("one two"), ["one", "two"])
        self.assertEqual(parse_tags("one two three"), ["one", "three", "two"])
        self.assertEqual(parse_tags("one one two two"), ["one", "two"])

    def test_with_comma_delimited_multiple_words(self):
        """
        Test with comma-delimited multiple words.
        An unquoted comma in the input will trigger this.
        """
        self.assertEqual(parse_tags(",one"), ["one"])
        self.assertEqual(parse_tags(",one two"), ["one two"])
        self.assertEqual(parse_tags(",one two three"), ["one two three"])
        self.assertEqual(
            parse_tags("a-one, a-two and a-three"), ["a-one", "a-two and a-three"]
        )

    def test_with_double_quoted_multiple_words(self):
        """
        Test with double-quoted multiple words.
        A completed quote will trigger this.  Unclosed quotes are ignored.
        """
        self.assertEqual(parse_tags('"one'), ["one"])
        self.assertEqual(parse_tags('"one two'), ["one", "two"])
        self.assertEqual(parse_tags('"one two three'), ["one", "three", "two"])
        self.assertEqual(parse_tags('"one two"'), ["one two"])
        self.assertEqual(
            parse_tags('a-one "a-two and a-three"'), ["a-one", "a-two and a-three"]
        )

    def test_with_no_loose_commas(self):
        """
        Test with no loose commas -- split on spaces.
        """
        self.assertEqual(parse_tags('one two "thr,ee"'), ["one", "thr,ee", "two"])

    def test_with_loose_commas(self):
        """
        Loose commas - split on commas
        """
        self.assertEqual(parse_tags('"one", two three'), ["one", "two three"])

    def test_tags_with_double_quotes_can_contain_commas(self):
        """
        Double quotes can contain commas
        """
        self.assertEqual(
            parse_tags('a-one "a-two, and a-three"'), ["a-one", "a-two, and a-three"]
        )
        self.assertEqual(parse_tags('"two", one, one, two, "one"'), ["one", "two"])

    def test_with_naughty_input(self):
        """
        Test with naughty input.
        """
        # Bad users! Naughty users!
        self.assertEqual(parse_tags(None), [])
        self.assertEqual(parse_tags(""), [])
        self.assertEqual(parse_tags('"'), [])
        self.assertEqual(parse_tags('""'), [])
        self.assertEqual(parse_tags('"' * 7), [])
        self.assertEqual(parse_tags(",,,,,,"), [])
        self.assertEqual(parse_tags('",",",",",",","'), [","])
        self.assertEqual(
            parse_tags('a-one "a-two" and "a-three'),
            ["a-one", "a-three", "a-two", "and"],
        )

    def test_recreation_of_tag_list_string_representations(self):
        plain = Tag(name="plain")
        spaces = Tag(name="spa ces")
        comma = Tag(name="com,ma")
        self.assertEqual(edit_string_for_tags([plain]), "plain")
        self.assertEqual(edit_string_for_tags([plain, spaces]), '"spa ces", plain')
        self.assertEqual(
            edit_string_for_tags([plain, spaces, comma]), '"com,ma", "spa ces", plain'
        )
        self.assertEqual(edit_string_for_tags([plain, comma]), '"com,ma", plain')
        self.assertEqual(edit_string_for_tags([comma, spaces]), '"com,ma", "spa ces"')

    @override_settings(TAGGIT_TAGS_FROM_STRING="tests.custom_parser.comma_splitter")
    def test_custom_comma_splitter(self):
        self.assertEqual(parse_tags("   Cued Speech "), ["Cued Speech"])
        self.assertEqual(parse_tags(" ,Cued Speech, "), ["Cued Speech"])
        self.assertEqual(parse_tags("Cued Speech"), ["Cued Speech"])
        self.assertEqual(
            parse_tags("Cued Speech, dictionary"), ["Cued Speech", "dictionary"]
        )

    @override_settings(TAGGIT_STRING_FROM_TAGS="tests.custom_parser.comma_joiner")
    def test_custom_comma_joiner(self):
        a = Tag(name="Cued Speech")
        b = Tag(name="transliterator")
        self.assertEqual(edit_string_for_tags([a, b]), "Cued Speech, transliterator")


class DeconstructTestCase(SimpleTestCase):
    def test_deconstruct_kwargs_kept(self):
        instance = TaggableManager(through=OfficialThroughModel, to="dummy.To")
        name, path, args, kwargs = instance.deconstruct()
        new_instance = TaggableManager(*args, **kwargs)
        self.assertEqual(
            "tests.OfficialThroughModel", new_instance.remote_field.through
        )
        self.assertEqual("dummy.To", new_instance.remote_field.model)


class InheritedPrefetchTests(TestCase):
    def test_inherited_tags_with_prefetch(self):
        child = Child()
        child.save()
        child.tags.add("tag 1", "tag 2", "tag 3", "tag 4")

        child = Child.objects.get()
        no_prefetch_tags = child.tags.all()
        self.assertEqual(4, no_prefetch_tags.count())
        child = Child.objects.prefetch_related("tags").get()
        prefetch_tags = child.tags.all()
        self.assertEqual(4, prefetch_tags.count())
        self.assertEqual(
            {t.name for t in no_prefetch_tags}, {t.name for t in prefetch_tags}
        )


class TagListViewTests(TestCase):
    model = Food

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.slug = "green"
        self.apple = self.model.objects.create(name="apple")
        self.apple.tags.add(self.slug)
        self.strawberry = self.model.objects.create(name="strawberry")
        self.strawberry.tags.add("red")

    def test_url_request_returns_view(self):
        request = self.factory.get("/food/tags/{}/".format(self.slug))
        queryset = self.model.objects.all()
        response = tagged_object_list(request, self.slug, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.apple, response.context_data["object_list"])
        self.assertNotIn(self.strawberry, response.context_data["object_list"])
        self.assertEqual(
            self.apple.tags.first(), response.context_data["extra_context"]["tag"]
        )

    def test_list_view_returns_single(self):
        response = self.client.get("/food/tags/{}/".format(self.slug))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.apple, response.context_data["object_list"])
        self.assertNotIn(self.strawberry, response.context_data["object_list"])


class RelatedNameTests(TestCase):
    def test_default_related_name(self):
        food = Food.objects.create(name="apple")
        food.tags.add("green")
        tag = Tag.objects.get(food=food.pk)
        self.assertEqual(tag.name, "green")

    def test_custom_related_name(self):
        name = Name.objects.create()
        name.tags.add("foo")
        tag = Tag.objects.get(a_unique_related_name=name.pk)
        self.assertEqual(tag.name, "foo")
