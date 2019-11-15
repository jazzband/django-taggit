# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(help_text='', unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('object_id', models.IntegerField(help_text='', verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='taggit_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType', help_text='', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='taggit_taggeditem_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Tagged Item',
                'verbose_name_plural': 'Tagged Items',
            },
            bases=(models.Model,),
        ),
    ]
