from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag, TaggedItem
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    args = '<tag_slug tag_slug ... destination_slug>'
    help = 'merges all tags into a single destination tag'

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError('At least two tag slugs must be provided')

        dest_slug = args[-1]
        try:
            dest_tag = Tag.objects.get(slug=dest_slug)
        except ObjectDoesNotExist:
            raise CommandError('Destination Tag "%s" does not exist' % dest_slug)

        for slug in args[:-1]:
            try:
                tag = Tag.objects.get(slug=slug)
            except ObjectDoesNotExist:
                raise CommandError('Tag "%s" does not exist' % slug)

            items = TaggedItem.objects.filter(tag=tag)
            count = items.count()
            for i, item in enumerate(items):
                if i % 20 == 0:
                    self.stdout.write('Merging %s %d/%d\n' % (slug, i+1, count))
                obj = item.content_object
                obj.tags.remove(tag)
                obj.tags.add(dest_tag)
            tag.delete()

            self.stdout.write('Successfully merged tags into "%s"\n' % dest_slug)