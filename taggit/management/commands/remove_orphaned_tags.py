from django.core.management.base import BaseCommand

from taggit.models import Tag


class Command(BaseCommand):
    help = "Remove orphaned tags"

    def handle(self, *args, **options):
        orphaned_tags = Tag.objects.filter(taggit_taggeditem_items=None)
        count = orphaned_tags.delete()
        self.stdout.write(f"Successfully removed {count} orphaned tags")
