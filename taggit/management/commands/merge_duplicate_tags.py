from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from taggit.services.tag_merging import TagMergingService


class Command(BaseCommand):
    help = "Merges duplicate tags, with options to specify tag and tagged item models."

    def add_arguments(self, parser):
        parser.add_argument(
            "tag_name", type=str, help="The name of the tag to merge duplicates for."
        )
        parser.add_argument(
            "--tag-model", type=str, help="The tag model to use.", default="taggit.Tag"
        )

    def handle(self, *args, **options):
        """
        Handles the command to merge duplicate tags.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments. Expected to contain:
                - tag_name (str): The name of the tag to merge duplicates for.
                - tag_model (str): The Django model path for the tag model.

        Raises:
            CommandError: If the specified tag does not exist or if an unspecified error occurs during
        """
        tag_name = options["tag_name"]
        tag_model_path = options["tag_model"]

        # Dynamic import of models
        TagModel = self.dynamic_import(tag_model_path)

        # Initialize the TagMergingService with the specified models

        service = TagMergingService(
            tag_model=TagModel,
        )

        try:
            service.merge_case_insensitive_tags(tag_name)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully merged duplicates of the tag "{tag_name}"'
                )
            )
        except TagModel.DoesNotExist:
            raise CommandError(f'Tag "{tag_name}" does not exist.')
        except Exception as e:
            raise CommandError(f"Error occurred while merging tags: {e}")

    @staticmethod
    def dynamic_import(app_label_model_name: str):
        """
        Dynamically imports a Django model given its 'app_label.model_name' string.
        """
        try:
            return apps.get_model(app_label_model_name)
        except LookupError:
            raise ImportError(
                f"No model found with app_label.model_name '{app_label_model_name}'"
            )
