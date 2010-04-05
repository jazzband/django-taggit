import re 
from django.db import models 
from django.core.exceptions import ValidationError 
from taggit.models import Tag 

class TagKeyword(models.Model): 
    """ Model to associate simple keywords to a Tag """ 
    tag = models.ForeignKey(Tag, related_name='keywords')
    keyword = models.CharField(max_length=30)

    def __unicode__(self): 
        return "Keyword '%s' for Tag '%s'" % (self.keyword, self.tag.name)

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
                             )
    case_insensitive = models.BooleanField(default=False)

    def __unicode__(self): 
        return self.name 
   
    def save(self, *args, **kwargs): 
        """ Make sure to validate """ 
        self.full_clean()
        super(TagRegExp,self).save(*args,**kwargs)
