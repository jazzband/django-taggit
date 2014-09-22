# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='object_id',
            field=models.CharField(max_length=255, verbose_name='object ID', db_index=True),
        ),
    ]
