from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from taggit.models import Tag, TaggedItem


class Command(BaseCommand):
    help = "Identify and remove duplicate tags based on case insensitivity"

    def handle(self, *args, **kwargs):
        if not getattr(settings, "TAGGIT_CASE_INSENSITIVE", False):
            self.stdout.write(
                self.style.ERROR("TAGGIT_CASE_INSENSITIVE is not enabled.")
            )
            return

        tags = Tag.objects.all()
        tag_dict = {}
        tagged_items_to_update = defaultdict(list)

        for tag in tags:
            lower_name = tag.name.lower()
            if lower_name in tag_dict:
                existing_tag = tag_dict[lower_name]
                self._collect_tagged_items(tag, existing_tag, tagged_items_to_update)
                tag.delete()
            else:
                tag_dict[lower_name] = tag

        self._remove_duplicates_and_update(tagged_items_to_update)
        self.stdout.write(self.style.SUCCESS("Tag deduplication complete."))

    def _collect_tagged_items(self, tag, existing_tag, tagged_items_to_update):
        for item in TaggedItem.objects.filter(tag=tag):
            tagged_items_to_update[(item.content_type_id, item.object_id)].append(
                existing_tag.id
            )

    def _remove_duplicates_and_update(self, tagged_items_to_update):
        with transaction.atomic():
            for (content_type_id, object_id), tag_ids in tagged_items_to_update.items():
                unique_tag_ids = set(tag_ids)
                if len(unique_tag_ids) > 1:
                    first_tag_id = unique_tag_ids.pop()
                    for duplicate_tag_id in unique_tag_ids:
                        TaggedItem.objects.filter(
                            content_type_id=content_type_id,
                            object_id=object_id,
                            tag_id=duplicate_tag_id,
                        ).delete()

                    TaggedItem.objects.filter(
                        content_type_id=content_type_id,
                        object_id=object_id,
                        tag_id=first_tag_id,
                    ).update(tag_id=first_tag_id)
