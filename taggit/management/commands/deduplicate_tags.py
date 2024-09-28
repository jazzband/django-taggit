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

        for tag in tags:
            lower_name = tag.name.lower()
            if lower_name in tag_dict:
                existing_tag = tag_dict[lower_name]
                self._deduplicate_tags(existing_tag=existing_tag, tag_to_remove=tag)
            else:
                tag_dict[lower_name] = tag

        self.stdout.write(self.style.SUCCESS("Tag deduplication complete."))

    @transaction.atomic
    def _deduplicate_tags(self, existing_tag, tag_to_remove):
        """
        Remove a tag by merging it into an existing tag
        """
        # If this ends up very slow for you, please file a ticket!
        # This isn't trying to be performant, in order to keep the code simple.
        for item in TaggedItem.objects.filter(tag=tag_to_remove):
            # if we already have the same association on the model
            # (via the existing tag), then we can just remove the
            # tagged item.
            tag_exists_other = TaggedItem.objects.filter(
                tag=existing_tag,
                content_type_id=item.content_type_id,
                object_id=item.object_id,
            ).exists()
            if tag_exists_other:
                item.delete()
            else:
                item.tag = existing_tag
                item.save()

        # this should never trigger, but can never be too sure
        assert not TaggedItem.objects.filter(
            tag=tag_to_remove
        ).exists(), "Tags were not all cleaned up!"

        tag_to_remove.delete()

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
