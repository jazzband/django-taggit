from django.test import TestCase 
from django.core.exceptions import ValidationError 
from taggit.models import Tag 
from taggit.contrib.suggest.models import TagKeyword, TagRegExp
from taggit.contrib.suggest.utils import suggest_tags 

class AddKeywordCase(TestCase): 
    def test_adding_keyword(self): 
        new_tag = Tag.objects.create(name='ku')
        new_keyword = TagKeyword.objects.create(
                            tag=new_tag, 
                            keyword='kansas university')
        self.assertTrue(new_keyword)
        self.assertTrue(new_keyword.tag == new_tag)
        
class AddRegexpCase(TestCase): 
    def test_adding_regexp(self): 
        new_tag = Tag.objects.create(name='ku')
        new_regexp = TagRegExp.objects.create(
                            tag=new_tag, 
                            name='Find University of Kansas',
                            regexp='University\s+of\s+Kansas')
        self.assertTrue(new_regexp)
        self.assertTrue(new_regexp.tag == new_tag) 

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

