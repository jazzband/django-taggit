from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Food


class AdminTest(TestCase):
    def setUp(self):
        super().setUp()
        self.apple = Food.objects.create(name="apple")
        self.apple.tags.add("Red", "red")
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
