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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('title', models.CharField(help_text='', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKFood',
            fields=[
                ('name', models.CharField(help_text='', max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKPet',
            fields=[
                ('name', models.CharField(help_text='', max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomPKHousePet',
            fields=[
                ('custompkpet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.CustomPKPet', help_text='', on_delete=models.CASCADE)),
                ('trained', models.BooleanField(default=False, help_text='')),
            ],
            options={
            },
            bases=('tests.custompkpet',),
        ),
        migrations.CreateModel(
            name='DirectCustomPKFood',
            fields=[
                ('name', models.CharField(help_text='', max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectCustomPKPet',
            fields=[
                ('name', models.CharField(help_text='', max_length=50, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectCustomPKHousePet',
            fields=[
                ('directcustompkpet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.DirectCustomPKPet', help_text='', on_delete=models.CASCADE)),
                ('trained', models.BooleanField(default=False, help_text='')),
            ],
            options={
            },
            bases=('tests.directcustompkpet',),
        ),
        migrations.CreateModel(
            name='DirectFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectPet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectHousePet',
            fields=[
                ('directpet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.DirectPet', help_text='', on_delete=models.CASCADE)),
                ('trained', models.BooleanField(default=False, help_text='')),
            ],
            options={
            },
            bases=('tests.directpet',),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleTagsGFK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('tags1', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialPet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialHousePet',
            fields=[
                ('officialpet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.OfficialPet', help_text='', on_delete=models.CASCADE)),
                ('trained', models.BooleanField(default=False, help_text='')),
            ],
            options={
            },
            bases=('tests.officialpet',),
        ),
        migrations.CreateModel(
            name='OfficialTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(help_text='', unique=True, max_length=100, verbose_name='Slug')),
                ('official', models.BooleanField(default=False, help_text='')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialThroughModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('object_id', models.IntegerField(help_text='', verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='tests_officialthroughmodel_tagged_items', verbose_name='Content type', to='contenttypes.ContentType', help_text='', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tagged_items', to='tests.OfficialTag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('parent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.Parent', help_text='', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=('tests.parent',),
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('name', models.CharField(help_text='', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HousePet',
            fields=[
                ('pet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tests.Pet', help_text='', on_delete=models.CASCADE)),
                ('trained', models.BooleanField(default=False, help_text='')),
            ],
            options={
            },
            bases=('tests.pet',),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedCustomPK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('object_id', models.CharField(help_text='', max_length=50, verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='tests_taggedcustompk_tagged_items', verbose_name='Content type', to='contenttypes.ContentType', help_text='', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_taggedcustompk_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedCustomPKFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.DirectCustomPKFood', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_taggedcustompkfood_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedCustomPKPet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.DirectCustomPKPet', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_taggedcustompkpet_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.DirectFood', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_taggedfood_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedPet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.DirectPet', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_taggedpet_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Through1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.MultipleTags', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_through1_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Through2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('content_object', models.ForeignKey(help_text='', to='tests.MultipleTags', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tests_through2_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThroughGFK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='', verbose_name='ID')),
                ('object_id', models.IntegerField(help_text='', verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='tests_throughgfk_tagged_items', verbose_name='Content type', to='contenttypes.ContentType', help_text='', on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='tagged_items', to='taggit.Tag', help_text='', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='officialpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='tests.OfficialTag', through='tests.OfficialThroughModel', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='officialfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='tests.OfficialTag', through='tests.OfficialThroughModel', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multipletagsgfk',
            name='tags2',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.ThroughGFK', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multipletags',
            name='tags1',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.Through1', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multipletags',
            name='tags2',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.Through2', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='custompkpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPK', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='custompkfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPK', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedPet', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedFood', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directcustompkpet',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPKPet', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directcustompkfood',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='tests.TaggedCustomPKFood', help_text='A comma-separated list of tags.', verbose_name='Tags'),
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
