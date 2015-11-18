# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taggeditem',
            unique_together=[('tag', 'content_type', 'object_id')],
        ),
    ]
