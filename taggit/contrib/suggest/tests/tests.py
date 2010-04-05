from django.test import TestCase 
from django.core.exceptions import ValidationError 
from taggit.models import Tag 
from taggit.contrib.suggest.models import TagKeyword, TagRegExp
from taggit.contrib.suggest.utils import suggest_tags 

class SuggestCase(TestCase): 
    def test_simple_suggest(self): 
        ku_tag = Tag.objects.create(name='ku')
        ku_keyword1 = TagKeyword.objects.create(
                            tag=ku_tag, 
                            keyword='kansas university')

        suggested_tags = suggest_tags(content='I used to be a student at kansas university')
        self.assertTrue(ku_tag in suggested_tags)

    def test_regexp_suggest(self): 
        ku_tag = Tag.objects.create(name='ku')
        new_regexp = TagRegExp.objects.create(
                            tag=ku_tag, 
                            name='Find University of Kansas',
                            regexp='University\s+of\s+Kansas')

        suggested_tags = suggest_tags(content='I was once a student at the University of Kansas')

        self.assertTrue(ku_tag in suggested_tags)

    def test_bad_regexp(self):
        ku_tag = Tag.objects.create(name='ku')
        ku_keyword1 = TagKeyword.objects.create(
                            tag=ku_tag, 
                            keyword='kansas university')
        new_regexp = TagRegExp(
                            tag=ku_tag, 
                            name='Find University of Kansas',
                            regexp='University\s+of(\s+Kansas')
        self.assertRaises(ValidationError, new_regexp.save)

        suggested_tags = suggest_tags(content='I was once a student at the University of Kansas. Also known as kansas university by the way.')

        self.assertTrue(ku_tag in suggested_tags)

