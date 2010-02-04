from django.db import models

from taggit.managers import TaggableManager


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