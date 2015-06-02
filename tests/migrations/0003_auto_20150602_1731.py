# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('tests', '0002_auto_20150602_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFKFoodNoRelatedName',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaggedCustomFKFoodNoRelatedName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='tests.CustomFKFoodNoRelatedName')),
                ('tag', models.ForeignKey(to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customfkfoodnorelatedname',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomFKFoodNoRelatedName', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
