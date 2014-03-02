# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=u'Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name=u'Slug')),
            ],
            options={
                u'verbose_name': u'Tag',
                u'verbose_name_plural': u'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(to='taggit.Tag', to_field=u'id')),
                ('object_id', models.IntegerField(verbose_name=u'Object id', db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', to_field=u'id', verbose_name=u'Content type')),
            ],
            options={
                u'verbose_name': u'Tagged Item',
                u'verbose_name_plural': u'Tagged Items',
            },
            bases=(models.Model,),
        ),
    ]
