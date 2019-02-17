from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("taggit", "0001_initial")]

    operations = [
        migrations.AlterIndexTogether(
            name="taggeditem", index_together={("content_type", "object_id")}
        )
    ]
