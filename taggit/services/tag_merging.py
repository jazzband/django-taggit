import logging

from django.apps import apps
from django.db import transaction
from django.db.models import QuerySet

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

logger = logging.getLogger(__name__)


class TagMergingService:
    @staticmethod
    def get_models_using_tag_through_models():
        """
        Retrieves a set of 'through' models used by TaggableManager fields across all registered models.

        Returns:
            set: A set of models that serve as 'through' models for TaggableManager fields.
        """
        return {
            field.through
            for model in apps.get_models()
            for field in model._meta.get_fields()
            if isinstance(field, TaggableManager)
        }

    def identify_duplicates(
        self, duplicate_query_set: QuerySet[TagBase], through_model
    ) -> QuerySet[GenericTaggedItemBase]:
        """
        Identifies TaggedItemBase instances associated with tags in the provided queryset.

        This method filters `GenericTaggedItemBase` instances to find those associated with any of the tags
        in the given `duplicate_query_set`.

        Args:
            duplicate_query_set (QuerySet[TagBase]): A queryset containing instances of TagBase
                considered duplicates.

        Returns:
            QuerySet[GenericTaggedItemBase]: A queryset of TagItems instances associated with the tags
                in `duplicate_query_set`.
        """

        return through_model.objects.filter(tag__in=duplicate_query_set)

    def tagged_item_exists(self, tagged_item, base_tag, through_model):
        """
        Checks if a tagged item already exists with the specified base tag.

        This method determines whether a `TaggedItem` instance associated with a given `tagged_item`
        already exists with the `base_tag`. It supports checking for existence based on two scenarios:
        - If the `tag_through_model` has a `content_type` attribute, it filters based on `content_type`,
          `object_id`, and `tag`.
        - If the `tag_through_model` does not have a `content_type` attribute, it filters based on
          `content_object` and `tag`.

        Args:
            tagged_item (GenericTaggedItemBase): The tagged item instance to check for an existing tag.
            base_tag (TagBase): The base tag to check against the tagged item.

        Returns:
            bool: True if an existing tagged item with the base tag is found, False otherwise.
        """
        if hasattr(through_model, "content_type"):
            return through_model.objects.filter(
                content_type=tagged_item.content_type,
                object_id=tagged_item.object_id,
                tag=base_tag,
            ).exists()
        return through_model.objects.filter(
            content_object=tagged_item.content_object,
            tag=base_tag,
        ).exists()

    def _merge_tags(
        self, base_tag: TagBase, duplicate_query_set: QuerySet[TagBase], through_model
    ) -> None:
        """
        Merges tags in the `duplicate_query_set` into a single `base_tag`.

        This method performs the merging of tags by first excluding the `base_tag`
        from the `duplicate_query_set` to ensure it is not deleted or modified.
        It then identifies all `TaggedItem` instances associated with the tags in
        the `duplicate_query_set` and updates their `tag_id` to point to the `base_tag`.
        Finally, it deletes all tags in the `duplicate_query_set`,
        effectively merging them into the `base_tag`.

        Args:
            base_tag: The tag into which all duplicates will be merged.
            duplicate_query_set: A queryset of tags considered duplicates
            that should be merged into the `base_tag`.

        """
        try:
            with transaction.atomic():
                duplicate_query_set = duplicate_query_set.exclude(pk=base_tag.pk)

                tags_to_be_merged_names = list(
                    duplicate_query_set.values_list("name", flat=True)
                )
                tag_to_update = self.identify_duplicates(
                    duplicate_query_set, through_model
                )
                for tagged_item in tag_to_update:
                    if not self.tagged_item_exists(
                        tagged_item, base_tag, through_model
                    ):
                        tagged_item.tag = base_tag
                        tagged_item.save()

                if tags_to_be_merged_names:
                    logger.info(
                        f"Merged tags {', '.join(tags_to_be_merged_names)} into {base_tag.name} and deleted them."
                    )
                else:
                    logger.info(
                        f"No tags were merged into {base_tag.name} as no duplicates were found."
                    )

        except Exception as e:
            logger.error(f"Error merging tags: {e}")
            raise

    @staticmethod
    def case_insensitive_queryset(tag_model, base_tag_name):
        return tag_model.objects.filter(name__iexact=base_tag_name)

    def merge_case_insensitive_tags(self, base_tag_name: str):
        """
        Merges all tags that match the `base_tag_name` case-insensitively into a single tag.

        This method finds all tags that match the given `base_tag_name` without considering case (case-insensitive match).
        It then merges all these tags into a single tag identified by the exact `base_tag_name`.
        This is useful for consolidating tags that are meant to be the same but may have been created with different
        case usage, ensuring data consistency and reducing redundancy.

        Raises:
            Tag.DoesNotExist: If no tag with the exact `base_tag_name` is found

        Args:
            base_tag_name (str): The name of the base tag into which all case-insensitive matches will be merged.
        """
        self.merge_tags(base_tag_name, self.case_insensitive_queryset)

    def merge_tags(self, base_tag_name, duplicate_query_function) -> None:
        """
        Merges all tags that match the `base_tag_name` into a single tag.

        The `base_tag_name` must exist in the database. If the `base_tag_name` does not exist tags will not be merged.

        This method finds all tags that match the given `base_tag_name` and merges them into a single tag
        identified by the exact `base_tag_name`. It uses the provided `duplicate_query_function` to determine
        the tags to merge based on the `base_tag_name`. The `duplicate_query_function` should accept two arguments:
        the tag model and the `base_tag_name`, and return a queryset of tags to merge into the `base_tag_name`.

        Args:
            base_tag_name (str): The name of the base tag into which all duplicates will be merged.
            duplicate_query_function (Callable): A function that accepts the tag model and the `base_tag_name`
                and returns a queryset of tags to merge into the `base_tag_name`.

        Raises:
            ValueError: If the `duplicate_query_function` is not
                callable.

        """
        if not callable(duplicate_query_function):
            raise ValueError("duplicate_query_function must be callable")
        tag_models = set()
        for through_model in self.get_models_using_tag_through_models():
            tag_model = through_model.tag_model()
            try:
                base_tag = tag_model.objects.get(name=base_tag_name)
            except tag_model.DoesNotExist:
                continue
            duplicate_query_set = duplicate_query_function(
                tag_model, base_tag_name
            ).exclude(name=base_tag_name)
            self._merge_tags(base_tag, duplicate_query_set, through_model)
            tag_models.add(tag_model)

        for tag_model in tag_models:
            duplicate_query_function(tag_model, base_tag_name).exclude(
                name=base_tag_name
            ).delete()
