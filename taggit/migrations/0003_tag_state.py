# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='state',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Published'), (1, 'Hidden')]),
        ),
    ]
