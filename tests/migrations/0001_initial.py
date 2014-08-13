# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKFood',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKPet',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKHousePet',
            fields=[
                ('custompkpet_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='tests.CustomPKPet')),
                ('trained', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('tests.custompkpet',),
        ),
        migrations.CreateModel(
            name='DirectFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectHousePet',
            fields=[
                ('directpet_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='tests.DirectPet')),
                ('trained', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('tests.directpet',),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleTagsGFK',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags1', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialHousePet',
            fields=[
                ('officialpet_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='tests.OfficialPet')),
                ('trained', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('tests.officialpet',),
        ),
        migrations.CreateModel(
            name='OfficialTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('official', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialThroughModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(to='tests.OfficialTag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='officialfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='tests.OfficialTag', through='tests.OfficialThroughModel', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='officialpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='tests.OfficialTag', through='tests.OfficialThroughModel', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HousePet',
            fields=[
                ('pet_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='tests.Pet')),
                ('trained', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('tests.pet',),
        ),
        migrations.AddField(
            model_name='pet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedCustomPKFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='custompkfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPKFood', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedcustompkfood',
            name='content_object',
            field=models.ForeignKey(to='tests.CustomPKFood'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedcustompkfood',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TaggedCustomPKPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='custompkpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPKPet', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedcustompkpet',
            name='content_object',
            field=models.ForeignKey(to='tests.CustomPKPet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedcustompkpet',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TaggedFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedFood', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedfood',
            name='content_object',
            field=models.ForeignKey(to='tests.DirectFood'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedfood',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TaggedPet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedPet', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedpet',
            name='content_object',
            field=models.ForeignKey(to='tests.DirectPet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taggedpet',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Through1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multipletags',
            name='tags1',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.Through1', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='through1',
            name='content_object',
            field=models.ForeignKey(to='tests.MultipleTags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='through1',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Through2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multipletags',
            name='tags2',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.Through2', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='through2',
            name='content_object',
            field=models.ForeignKey(to='tests.MultipleTags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='through2',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ThroughGFK',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multipletagsgfk',
            name='tags2',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.ThroughGFK', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='ArticleTaggedItem',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.taggeditem',),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.ArticleTaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
