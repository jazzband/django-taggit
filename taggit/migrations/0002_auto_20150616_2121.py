from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("taggit", "0001_initial")]

    operations = [
        migrations.AddIndex(
            "taggeditem",
            models.Index(
                fields=("content_type", "object_id"),
                # this is not the name of the index in previous version,
                # but this is ncessary to deal with index_together issues.
                name="taggit_tagg_content_8fc721_idx",
            ),
        )
    ]
