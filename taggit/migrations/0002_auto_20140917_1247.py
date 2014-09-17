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
            name='content_type',
            field=models.ForeignKey(related_name='taggit_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.ForeignKey(related_name='taggit_taggeditem_items', to='taggit.Tag'),
        ),
    ]
