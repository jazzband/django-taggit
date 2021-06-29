import django
from rest_framework import serializers

from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import TestModel


class TestModelSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = TestModel
        if django.VERSION >= (1, 11):
            fields = "__all__"
