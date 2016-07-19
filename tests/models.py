from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager
from taggit.models import (CommonGenericTaggedItemBase, GenericTaggedItemBase,
                           Tag, TagBase, TaggedItem, TaggedItemBase)


# Ensure that two TaggableManagers with custom through model are allowed.
class Through1(TaggedItemBase):
    content_object = models.ForeignKey('MultipleTags', on_delete=models.CASCADE)


class Through2(TaggedItemBase):
    content_object = models.ForeignKey('MultipleTags', on_delete=models.CASCADE)


class MultipleTags(models.Model):
    tags1 = TaggableManager(through=Through1, related_name='tags1')
    tags2 = TaggableManager(through=Through2, related_name='tags2')


# Ensure that two TaggableManagers with GFK via different through models are allowed.
class ThroughGFK(GenericTaggedItemBase):
    tag = models.ForeignKey(Tag, related_name='tagged_items', on_delete=models.CASCADE)


class MultipleTagsGFK(models.Model):
    tags1 = TaggableManager(related_name='tagsgfk1')
    tags2 = TaggableManager(through=ThroughGFK, related_name='tagsgfk2')


@python_2_unicode_compatible
class Food(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Pet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class HousePet(Pet):
    trained = models.BooleanField(default=False)


# Test direct-tagging with custom through model

class TaggedFood(TaggedItemBase):
    content_object = models.ForeignKey('DirectFood', on_delete=models.CASCADE)


class TaggedPet(TaggedItemBase):
    content_object = models.ForeignKey('DirectPet', on_delete=models.CASCADE)


@python_2_unicode_compatible
class DirectFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through='TaggedFood')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DirectPet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedPet)

    def __str__(self):
        return self.name


class DirectHousePet(DirectPet):
    trained = models.BooleanField(default=False)


# Test custom through model to model with custom PK

class TaggedCustomPKFood(TaggedItemBase):
    content_object = models.ForeignKey('DirectCustomPKFood', on_delete=models.CASCADE)


class TaggedCustomPKPet(TaggedItemBase):
    content_object = models.ForeignKey('DirectCustomPKPet', on_delete=models.CASCADE)


@python_2_unicode_compatible
class DirectCustomPKFood(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPKFood)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DirectCustomPKPet(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPKPet)

    def __str__(self):
        return self.name


class DirectCustomPKHousePet(DirectCustomPKPet):
    trained = models.BooleanField(default=False)


# Test custom through model to model with custom PK using GenericForeignKey
class TaggedCustomPK(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name='Object id', db_index=True)


@python_2_unicode_compatible
class CustomPKFood(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPK)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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
    tag = models.ForeignKey(OfficialTag, related_name="tagged_items", on_delete=models.CASCADE)


@python_2_unicode_compatible
class OfficialFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=OfficialThroughModel)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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
    class Foo(object):
        def __init__(*args, **kwargs):
            pass

    tags = TaggableManager(manager=Foo)


class Parent(models.Model):
    tags = TaggableManager()


class Child(Parent):
    pass
