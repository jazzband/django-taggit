# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFKFood',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaggedCustomFKFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='tests.CustomFKFood')),
                ('tag', models.ForeignKey(related_name='custom_fk_food', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customfkfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomFKFood', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
