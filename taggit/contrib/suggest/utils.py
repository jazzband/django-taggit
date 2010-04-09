import re 
from taggit.models import Tag 
from taggit.contrib.suggest.models import TagKeyword, TagRegExp
from django.conf import settings 


def _suggest_keywords(content=None):
    """ Suggest by keywords """ 
    suggested_keywords = set()
    keywords = TagKeyword.objects.values_list('keyword', 'tag')

    for k in keywords: 
        if k[0] in content: 
            suggested_keywords.add(k[1])

    return suggested_keywords 

def _suggest_regexps(content=None): 
    """ Suggest by regular expressions """ 
    # Grab all regular expressions and compile them 
    suggested_regexps = set()
    regexps = set()
    regexp_keywords = TagRegExp.objects.values_list(
                            'regexp', 
                            'tag', 
                            )

    for r in regexp_keywords: 
        regexps.add((re.compile(r[0]), r[1]))

    # Look for our regular expressions in the content 
    for r in regexps:
        if r[0].search(content):
            suggested_regexps.add(r[1])

    return suggested_regexps 

def suggest_tags(content=None):
    """ Suggest tags based on text content """ 
    suggested_keywords = _suggest_keywords(content)
    suggested_regexps  = _suggest_regexps(content) 
    suggested_tag_ids  = suggested_keywords | suggested_regexps

    return Tag.objects.filter(id__in=suggested_tag_ids)
