from rest_framework import serializers
import django
from .models import TestModel
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class TestModelSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = TestModel
        if django.VERSION >= (1, 11):
            fields = "__all__"
