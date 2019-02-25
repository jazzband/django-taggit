# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("tests", "0002_uuid_models"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="taggedfood", unique_together={("content_object", "tag")}
        ),
        migrations.AlterUniqueTogether(
            name="taggedcustompkfood", unique_together={("content_object", "tag")}
        ),
        migrations.AlterUniqueTogether(
            name="taggedcustompkpet", unique_together={("content_object", "tag")}
        ),
        migrations.AlterUniqueTogether(
            name="taggedcustompk", unique_together={("object_id", "tag")}
        ),
        migrations.AlterUniqueTogether(
            name="officialthroughmodel",
            unique_together={("content_type", "object_id", "tag")},
        ),
    ]
