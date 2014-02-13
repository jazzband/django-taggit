from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag

class Command(BaseCommand):
    args = 'none'
    help = 'all tag names'

    def handle(self, *args, **options):
        tags = Tag.objects.all()
        count = tags.count()
        for i, tag in enumerate(tags):
            if i % 20 == 0:
                self.stdout.write('Lowercasing %d/%d\n' % (i+1, count))
            tag.name = tag.name.lower()
            tag.save()