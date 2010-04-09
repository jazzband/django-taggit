import re 

from django.db import models 
from django.core.exceptions import ValidationError 
from taggit.models import Tag 

HAS_PYSTEMMER = True 
try: 
    import Stemmer
except ImportError: 
    HAS_PYSTEMMER = False 

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
        if not self.id and not self.stem and HAS_PYSTEMMER: 
            stemmer = Stemmer.Stemmer(language)
            self.stem = stemmer.stemWord(self.keyword)
        super(TagKeyword,self).save(*args,**kwargs)

def validate_regexp(value): 
    """ Make sure we have a valid regular expression """ 
    try: 
        re.compile(value)
    except:
        raise ValidationError('Please enter a valid regular expression')

class TagRegExp(models.Model): 
    """ Model to associate regular expressions with a Tag """ 
    tag = models.ForeignKey(Tag, related_name='regexps')
    name = models.CharField(max_length=30)
    regexp = models.CharField(max_length=250,
                             validators=[validate_regexp],
                             help_text='Enter a valid Regular Expression. To make it case-insensitive include "(?i)" in your expression.'
                             )

    def __unicode__(self): 
        return self.name 
   
    def save(self, *args, **kwargs): 
        """ Make sure to validate """ 
        self.full_clean()
        super(TagRegExp,self).save(*args,**kwargs)
