"""
test_django-taggit-serializer
------------

Tests for `django-taggit-serializer` models module.
"""

import unittest

from rest_framework.exceptions import ValidationError

from taggit import serializers

from .models import TestModel
from .serializers import TestModelSerializer


class TestTaggit_serializer(unittest.TestCase):
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
        serializer.is_valid()
        test_model = serializer.save()

        assert len(test_model.tags.all()) == len(request_data.get("tags"))

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
