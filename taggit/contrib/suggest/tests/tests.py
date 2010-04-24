from django.core.exceptions import ValidationError
from django.test import TestCase

from taggit.contrib.suggest.models import TagKeyword, TagRegex
from taggit.contrib.suggest.utils import suggest_tags
from taggit.models import Tag


class SuggestCase(TestCase):
    def test_simple_suggest(self):
        ku_tag = Tag.objects.create(name='ku')
        ku_keyword1 = TagKeyword.objects.create(
            tag=ku_tag,
            keyword='kansas university'
        )

        suggested_tags = suggest_tags('I used to be a student at kansas university')
        self.assertTrue(ku_tag in suggested_tags)

    def test_regex_suggest(self):
        ku_tag = Tag.objects.create(name='ku')
        TagRegex.objects.create(
            tag=ku_tag,
            name='Find University of Kansas',
            regex='University\s+of\s+Kansas'
        )

        suggested_tags = suggest_tags('I was once a student at the University of Kansas')

        self.assertTrue(ku_tag in suggested_tags)

    def test_bad_regex(self):
        ku_tag = Tag.objects.create(name='ku')
        ku_keyword1 = TagKeyword.objects.create(
            tag=ku_tag,
            keyword='kansas university'
        )
        new_regex = TagRegex(
            tag=ku_tag,
            name='Find University of Kansas',
            regex='University\s+of(\s+Kansas'
        )
        self.assertRaises(ValidationError, new_regex.save)

        suggested_tags = suggest_tags('I was once a student at the University '
            'of Kansas. Also known as kansas university by the way.')

        self.assertTrue(ku_tag in suggested_tags)
