from django.core.management.base import BaseCommand, CommandError

from taggit.services.tag_merging import TagMergingService


class Command(BaseCommand):
    help = "Merges Tags with the same name but different case."

    def add_arguments(self, parser):
        parser.add_argument(
            "tag_name", type=str, help="The name of the tag to merge duplicates for."
        )

    def handle(self, *args, **options):
        """
        Handles the command to merge duplicate tags.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments. Expected to contain:
                - tag_name (str): The name of the tag to merge duplicates for.


        Raises:
            CommandError: If the specified tag does not exist or if an unspecified error occurs during
        """
        tag_name = options["tag_name"]
        service = TagMergingService()

        try:
            service.merge_case_insensitive_tags(tag_name)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully merged duplicates of the tag "{tag_name}"'
                )
            )
        except Exception as e:
            raise CommandError(f"Error occurred while merging tags: {e}")
