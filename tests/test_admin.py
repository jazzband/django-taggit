from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from taggit.models import Tag

from .models import Food


class AdminTest(TestCase):
    def setUp(self):
        super().setUp()
        self.apple = Food.objects.create(name="apple")
        self.apple.tags.add("Red", "red")
        self.pear = Food.objects.create(name="pear")
        self.pear.tags.add("red", "RED")
        self.peach = Food.objects.create(name="peach")
        self.peach.tags.add("red", "Yellow")

        user = User.objects.create_superuser(
            username="admin", email="admin@mailinator.com", password="password"
        )
        self.client.force_login(user)

    def test_get_changelist(self):
        response = self.client.get(reverse("admin:tests_food_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_get_add(self):
        response = self.client.get(reverse("admin:tests_food_add"))
        self.assertEqual(response.status_code, 200)

    def test_get_history(self):
        response = self.client.get(
            reverse("admin:tests_food_history", args=(self.apple.pk,))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_delete(self):
        response = self.client.get(
            reverse("admin:tests_food_delete", args=(self.apple.pk,))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_change(self):
        response = self.client.get(
            reverse("admin:tests_food_change", args=(self.apple.pk,))
        )
        self.assertEqual(response.status_code, 200)

    def test_tag_merging(self):
        response = self.client.get(reverse("admin:taggit_tag_changelist"))

        # merging red and RED into Red
        pks_to_select = [Tag.objects.get(name="red").pk, Tag.objects.get(name="RED").pk]
        response = self.client.post(
            reverse("admin:taggit_tag_changelist"),
            data={"action": "render_tag_form", "_selected_action": pks_to_select},
        )
        # we're redirecting
        self.assertEqual(response.status_code, 302)
        # make sure what we expected got into the session keys
        assert "selected_tag_ids" in self.client.session.keys()
        self.assertEqual(
            self.client.session["selected_tag_ids"], ",".join(map(str, pks_to_select))
        )

        # let's do the actual merge operation
        response = self.client.post(
            reverse("admin:taggit_tag_merge_tags"), {"new_tag_name": "Red"}
        )
        self.assertEqual(response.status_code, 302)

        # time to check the result of the merges
        self.assertSetEqual({tag.name for tag in self.apple.tags.all()}, {"Red"})
        self.assertSetEqual({tag.name for tag in self.pear.tags.all()}, {"Red"})
        self.assertSetEqual(
            {tag.name for tag in self.peach.tags.all()}, {"Yellow", "Red"}
        )
