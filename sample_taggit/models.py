#!/usr/bin/env python3
from django.db import models

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    tags = TaggableManager(blank=True)
