from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

class Food(models.Model):
    name = models.CharField(max_length=50)
    
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=50)
    
    tags = TaggableManager()

class HousePet(Pet):
    trained = models.BooleanField()

# test direct-tagging with custom through model
    
class TaggedFood(TaggedItemBase):
    content_object = models.ForeignKey('DirectFood')
    
class DirectFood(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedFood)

class TaggedPet(TaggedItemBase):
    content_object = models.ForeignKey('DirectPet')
    
class DirectPet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(through=TaggedPet)

class DirectHousePet(DirectPet):
    trained = models.BooleanField()

# test custom through model to model with custom PK

class TaggedCustomPKFood(TaggedItemBase):
    content_object = models.ForeignKey('CustomPKFood')

class CustomPKFood(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPKFood)
    
    def __unicode__(self):
        return self.name
    
class TaggedCustomPKPet(TaggedItemBase):
    content_object = models.ForeignKey('CustomPKPet')
    
class CustomPKPet(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    tags = TaggableManager(through=TaggedCustomPKPet)

class CustomPKHousePet(CustomPKPet):
    trained = models.BooleanField()
