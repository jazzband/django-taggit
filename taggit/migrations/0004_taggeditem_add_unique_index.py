# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("taggit", "0003_rm_unique_tagname"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="taggeditem", unique_together={("content_type", "object_id", "tag")}
        )
    ]
