from django.db import models

from taggit.managers import TaggableManager


class Food(models.Model):
    name = models.CharField(max_length=50)
    
    tags = TaggableManager()
