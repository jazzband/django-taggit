import uuid

from django.db import models

from taggit.managers import TaggableManager
from taggit.models import (
    CommonGenericTaggedItemBase,
    GenericTaggedItemBase,
    TagBase,
    TaggedItemBase,
)


class GenericTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        "GenericTag", related_name="tagged_items", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class GenericTag(TagBase):
    class Meta:
        abstract = True


class GenericModel(models.Model):
    name = models.CharField(max_length=50)
    tags = TaggableManager(through=GenericTaggedItem)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# Custom tag model
class CustomTag(TagBase):
    description = models.TextField(blank=True, max_length=255, null=True)

    class Meta:
        abstract = True


class CustomTaggedItem(TaggedItemBase):
    tag = models.ForeignKey(
        CustomTag, related_name="tagged_items", on_delete=models.CASCADE
    )
    content_object = models.ForeignKey("CustomTagModel", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CustomTagModel(models.Model):
    name = models.CharField(max_length=50)
    tags = TaggableManager(through=CustomTaggedItem)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CustomPKModel(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class TaggedCustomPK(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name="Object id", db_index=True)

    class Meta:
        abstract = True
        unique_together = [["object_id", "tag"]]
