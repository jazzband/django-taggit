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
