import uuid

from django.db import models

from taggit.managers import TaggableManager
from taggit.models import (
    CommonGenericTaggedItemBase,
    GenericTaggedItemBase,
    GenericUUIDTaggedItemBase,
    ItemBase,
    Tag,
    TagBase,
    TaggedItem,
    TaggedItemBase,
)


# Ensure that two TaggableManagers with custom through model are allowed.
class Through1(TaggedItemBase):
    content_object = models.ForeignKey("MultipleTags", on_delete=models.CASCADE)


class Through2(TaggedItemBase):
    content_object = models.ForeignKey("MultipleTags", on_delete=models.CASCADE)


class MultipleTags(models.Model):
    tags1 = TaggableManager(through=Through1, related_name="tags1")
    tags2 = TaggableManager(through=Through2, related_name="tags2")


# Ensure that two TaggableManagers with GFK via different through models are allowed.
class ThroughGFK(GenericTaggedItemBase):
    tag = models.ForeignKey(Tag, related_name="tagged_items", on_delete=models.CASCADE)


class MultipleTagsGFK(models.Model):
    tags1 = TaggableManager(related_name="tagsgfk1")
    tags2 = TaggableManager(through=ThroughGFK, related_name="tagsgfk2")


class BlankTagModel(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class BaseFood(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MultiInheritanceLazyResolutionFoodTag(TaggedItemBase):
    content_object = models.ForeignKey(
        "MultiInheritanceFood", related_name="tagged_items", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["content_object", "tag"]]


class MultiInheritanceFood(BaseFood):
    tags = TaggableManager(through=MultiInheritanceLazyResolutionFoodTag)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class HousePet(Pet):
    trained = models.BooleanField(default=False)


# Test direct-tagging with custom through model


class TaggedFood(TaggedItemBase):
    content_object = models.ForeignKey("DirectFood", on_delete=models.CASCADE)

    class Meta:
        unique_together = [["content_object", "tag"]]


class TaggedPet(TaggedItemBase):
    content_object = models.ForeignKey("DirectPet", on_delete=models.CASCADE)


class DirectFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through="TaggedFood")

    def __str__(self):
        return self.name


class DirectPet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedPet)

    def __str__(self):
        return self.name


class DirectHousePet(DirectPet):
    trained = models.BooleanField(default=False)


# Test direct-tagging with custom through model and custom tag


class TrackedTag(TagBase):
    created_by = models.CharField(max_length=50)
    created_dt = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, max_length=255, null=True)


class TaggedTrackedFood(ItemBase):
    content_object = models.ForeignKey("DirectTrackedFood", on_delete=models.CASCADE)
    tag = models.ForeignKey(
        TrackedTag, on_delete=models.CASCADE, related_name="%(class)s_items"
    )
    created_by = models.CharField(max_length=50)
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["content_object", "tag"]


class TaggedTrackedPet(ItemBase):
    content_object = models.ForeignKey("DirectTrackedPet", on_delete=models.CASCADE)
    tag = models.ForeignKey(
        TrackedTag, on_delete=models.CASCADE, related_name="%(class)s_items"
    )
    created_by = models.CharField(max_length=50)
    created_dt = models.DateTimeField(auto_now_add=True)


class DirectTrackedFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedTrackedFood)

    def __str__(self):
        return self.name


class DirectTrackedPet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedTrackedPet)

    def __str__(self):
        return self.name


class DirectTrackedHousePet(DirectTrackedPet):
    trained = models.BooleanField(default=False)


# Test custom through model to model with custom PK


class TaggedCustomPKFood(TaggedItemBase):
    content_object = models.ForeignKey("DirectCustomPKFood", on_delete=models.CASCADE)

    class Meta:
        unique_together = [["content_object", "tag"]]


class TaggedCustomPKPet(TaggedItemBase):
    content_object = models.ForeignKey("DirectCustomPKPet", on_delete=models.CASCADE)

    class Meta:
        unique_together = [["content_object", "tag"]]


class DirectCustomPKFood(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    tags = TaggableManager(through=TaggedCustomPKFood)

    def __str__(self):
        return self.name


class DirectCustomPKPet(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPKPet)

    def __str__(self):
        return self.name


class DirectCustomPKHousePet(DirectCustomPKPet):
    trained = models.BooleanField(default=False)


# Test custom through model to model with custom PK using GenericForeignKey
class TaggedCustomPK(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name="Object id", db_index=True)

    class Meta:
        unique_together = [["object_id", "tag"]]


class CustomPKFood(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPK)

    def __str__(self):
        return self.name


class CustomPKPet(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPK)

    def __str__(self):
        return self.name


class CustomPKHousePet(CustomPKPet):
    trained = models.BooleanField(default=False)


# Test custom through model to a custom tag model


class OfficialTag(TagBase):
    official = models.BooleanField(default=False)


class OfficialThroughModel(GenericTaggedItemBase):
    tag = models.ForeignKey(
        OfficialTag, related_name="tagged_items", on_delete=models.CASCADE
    )
    extra_field = models.CharField(max_length=10)

    class Meta:
        unique_together = [["content_type", "object_id", "tag"]]


class OfficialFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=OfficialThroughModel)

    def __str__(self):
        return self.name


class OfficialPet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=OfficialThroughModel)

    def __str__(self):
        return self.name


class OfficialHousePet(OfficialPet):
    trained = models.BooleanField(default=False)


class Media(models.Model):
    tags = TaggableManager()

    class Meta:
        abstract = True


class Photo(Media):
    pass


class Movie(Media):
    pass


class ProxyPhoto(Photo):
    class Meta:
        proxy = True


class ArticleTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        slug = "category-%s" % tag.lower()

        if i is not None:
            slug += "-%d" % i
        return slug


class ArticleTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(self):
        return ArticleTag


class Article(models.Model):
    title = models.CharField(max_length=100)

    tags = TaggableManager(through=ArticleTaggedItem)


class CustomManager(models.Model):
    class Foo:
        def __init__(*args, **kwargs):
            pass

    tags = TaggableManager(manager=Foo)


class Parent(models.Model):
    tags = TaggableManager()


class Child(Parent):
    pass


class UUIDFood(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    tags = TaggableManager(through="UUIDTaggedItem")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        # With a UUIDField pk, objects are not always ordered by creation time. So explicitly set ordering.
        ordering = ["created_at"]


class UUIDPet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    tags = TaggableManager(through="UUIDTaggedItem")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        # With a UUIDField pk, objects are not always ordered by creation time. So explicitly set ordering.
        ordering = ["created_at"]


class UUIDHousePet(UUIDPet):
    trained = models.BooleanField(default=False)


class UUIDTag(TagBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class UUIDTaggedItem(GenericUUIDTaggedItemBase):
    tag = models.ForeignKey(
        UUIDTag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["content_type", "object_id", "tag"]]


# Exists to verify system check failure.
# tests.Name.tags: (fields.E303) Reverse query name for 'Name.tags' clashes with field name 'Tag.name'.
# 	HINT: Rename field 'Tag.name', or add/change a related_name argument to the definition for field 'Name.tags'.
class Name(models.Model):
    tags = TaggableManager(related_name="a_unique_related_name")
