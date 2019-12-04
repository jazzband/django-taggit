from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("taggit", "0002_auto_20150616_2121"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="taggeditem", unique_together={("content_type", "object_id", "tag")}
        )
    ]
