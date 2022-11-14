"""
test_django-taggit-serializer
------------

Tests for `django-taggit-serializer` models module.
"""

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from taggit import serializers

from .models import TestModel
from .serializers import TestModelSerializer


class TestTaggit_serializer(TestCase):
    def test_taggit_serializer_field(self):
        correct_value = ["1", "2", "3"]
        serializer_field = serializers.TagListSerializerField()

        correct_value = serializer_field.to_internal_value(correct_value)

        assert type(correct_value) is list

        incorrect_value = "123"

        with self.assertRaises(ValidationError):
            incorrect_value = serializer_field.to_internal_value(incorrect_value)

        representation = serializer_field.to_representation(correct_value)
        self.assertIsInstance(representation, serializers.TagList)

    def test_taggit_serializer_update(self):
        """Test if serializer class is working properly on updating object"""
        request_data = {"tags": ["1", "2", "3"]}

        test_model = TestModel.objects.create()

        serializer = TestModelSerializer(test_model, data=request_data)
        serializer.is_valid()
        serializer.save()

        assert len(test_model.tags.all()) == len(request_data.get("tags"))

    def test_taggit_serializer_create(self):
        """
        Test if serializer class is working
        properly on creating a object
        """
        request_data = {"tags": ["1", "2", "3"]}

        serializer = TestModelSerializer(data=request_data)
        assert serializer.is_valid()
        test_model = serializer.save()

        assert len(test_model.tags.all()) == len(request_data.get("tags"))

    def test_taggit_serializer_create_with_string(self):
        """
        Test that we can pass in a string instead of an array for
        a tag list without issues
        """
        request_data = {"tags": '["1", "2", "3"]'}

        serializer = TestModelSerializer(data=request_data)
        assert serializer.is_valid(), serializer.errors
        test_model = serializer.save()

        assert set(tag.name for tag in test_model.tags.all()) == {"1", "2", "3"}

    def test_taggit_removes_tags(self):
        """
        Test if the old assigned tags are removed
        """
        test_model = TestModel.objects.create()
        test_model.tags.add("1")

        request_data = {"tags": ["2", "3"]}

        serializer = TestModelSerializer(test_model, data=request_data)
        serializer.is_valid()
        test_model = serializer.save()

        assert TestModel.objects.filter(tags__name__in=["1"]).count() == 0
        assert TestModel.objects.filter(tags__name__in=["1", "2"]).count() == 1

    def test_returns_new_data_after_update(self):
        """
        Test if the serializer uses fresh data after updating prefetched fields
        """
        TestModel.objects.create().tags.add("1")

        test_model = TestModel.objects.prefetch_related("tags").get()

        assert TestModelSerializer(test_model).data["tags"] == ["1"]

        request_data = {"tags": ["2", "3"]}
        serializer = TestModelSerializer(test_model, data=request_data)
        serializer.is_valid()
        test_model = serializer.save()

        assert set(serializer.data["tags"]) == {"2", "3"}
