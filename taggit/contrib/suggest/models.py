import re

from django.core.exceptions import ValidationError
from django.db import models

from taggit.models import Tag

try:
    import Stemmer
except ImportError:
    Stemmer = None


class TagKeyword(models.Model):
    """ Model to associate simple keywords to a Tag """
    tag = models.ForeignKey(Tag, related_name='keywords')
    keyword = models.CharField(max_length=30)
    stem = models.CharField(max_length=30)

    def __unicode__(self):
        return "Keyword '%s' for Tag '%s'" % (self.keyword, self.tag.name)

    def save(self, *args, **kwargs):
        """ Stem the keyword on save if they have PyStemmer """
        language = kwargs.pop('stemmer-language', 'english')
        if not self.pk and not self.stem and Stemmer:
            stemmer = Stemmer.Stemmer(language)
            self.stem = stemmer.stemWord(self.keyword)
        super(TagKeyword, self).save(*args, **kwargs)


def validate_regex(value):
    """ Make sure we have a valid regular expression """
    try:
        re.compile(value)
    except Exception:
        raise ValidationError('Please enter a valid regular expression')


class TagRegex(models.Model):
    """ Model to associate regular expressions with a Tag """
    tag = models.ForeignKey(Tag, related_name='regexes')
    name = models.CharField(max_length=30)
    regex = models.CharField(
        max_length=250,
         validators=[validate_regex],
         help_text=('Enter a valid Regular Expression. To make it '
            'case-insensitive include "(?i)" in your expression.')
     )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Make sure to validate """
        self.full_clean()
        super(TagRegex,self).save(*args, **kwargs)
