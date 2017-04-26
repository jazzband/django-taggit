from django.core.management.base import NoArgsCommand

try:
    import tagging
    import taggit
except ImportError, e:

    class Command(NoArgsCommand):
        def handle_noargs(self, **kwargs):
            print "Missing tag-library, aborting: %s" % e

else:
    from tagging.models import Tag as OldTag
    from taggit.models import Tag as NewTag
    from tagging.models import TaggedItem as OldTaggedItem
    from taggit.models import TaggedItem as NewTaggedItem

    class Command(NoArgsCommand):
        def handle_noargs(self, **kwargs):
            NewTag.objects.all().delete()
            NewTaggedItem.objects.all().delete()
            self.delete_unused_tags()
            self.set_tags()
            self.set_taggeditems()

        def get_used_tags(self):
            return tuple(set(t[0] for t in
                    OldTaggedItem.objects.only('tag').values_list('tag')))

        def delete_unused_tags(self):
            used_tags = self.get_used_tags()

            for t in tuple(OldTag.objects.all()):
                if t.id not in used_tags:
                    t.delete()
                    print "Deleted: %s (%s)" % (t.id, t.name)

        def set_tags(self):
            has_dupes = {}
            for old_tag in OldTag.objects.all():
                new_tag = NewTag(id=old_tag.id, name=old_tag.name)
                slug = new_tag.slugify(old_tag.name)
                try:
                    new_tag = NewTag.objects.get(slug=slug)
                    has_dupes.setdefault(new_tag.id, []).append(old_tag.id)
                    print 'ERROR: %s (%i,%i) already exists' % (slug, new_tag.id, old_tag.id)
                except NewTag.DoesNotExist:
                    new_tag.slug = slug
                    new_tag.save()
            self.dupemap = {}
            for first, later in has_dupes.items():
                for dupe in later:
                    self.dupemap[dupe] = first
            print '%i dupes' % len(self.dupemap)

        def set_taggeditems(self):
            objects = OldTaggedItem.objects.all()
            print objects.count()
            for old_tagitem in objects:
                old_id = old_tagitem.tag_id
                new_id = self.dupemap.get(old_id, old_id)
                new_tags = NewTag.objects.filter(id=new_id)
                if new_tags:
                    new_tag = new_tags[0]
                    new_tagitem = NewTaggedItem(
                            id=old_tagitem.id, 
                            tag=new_tag,
                            content_type=old_tagitem.content_type,
                            object_id=old_tagitem.object_id)
                    new_tagitem.save()
            print NewTaggedItem.objects.count()
