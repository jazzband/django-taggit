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
            name='SubmodelManagerPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmodelManegerHousePet',
            fields=[
                ('submodelmanagerpet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.SubmodelManagerPet')),
                ('trained', models.BooleanField(default=False)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=('tests.submodelmanagerpet',),
        ),
    ]
