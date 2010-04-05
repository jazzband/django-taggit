import re 
from taggit.models import Tag 
from taggit.contrib.suggest.models import TagKeyword, TagRegExp
from django.conf import settings 

HAS_NLTK = True 
try: 
    from nltk.stemmer.porter import PorterStemmer
except ImportError: 
    HAS_NLTK = False 

def _suggest_keywords(content=None):
    """ Suggest by keywords """ 
    suggested_keywords = set()
    keywords = TagKeyword.objects.values_list('keyword', 'tag')

    for k in keywords: 
        if k[0] in content: 
            suggested_keywords.add(str(k[1]))

    return suggested_keywords 

def _suggest_regexps(content=None): 
    """ Suggest by regular expressions """ 
    # Grab all regular expressions and compile them 
    suggested_regexps = set()
    regexps = set()
    regexp_keywords = TagRegExp.objects.values_list(
                            'regexp', 
                            'tag', 
                            'case_insensitive')

    for r in regexp_keywords: 
        try: 
            if r[2]: 
                reg = re.compile(r[0], re.IGNORE_CASE)
            else:
                reg = re.compile(r[0])
        except: 
            # Skip any badly formed regular expressions silently 
            continue 
        regexps.add((reg,r[1]))

    # Look for our regular expressions in the content 
    for r in regexps:
        if r[0].search(content):
            suggested_regexps.add(str(r[1]))

    return suggested_regexps 

def suggest_tags(content=None):
    """ Suggest tags based on text content """ 

    if not content: 
        return

    MAX_LENGTH = getattr(settings, 'TAGGIT_SUGGEST_MAX_LENGTH', None)
    if MAX_LENGTH: 
        content = content[0:settings.TAGGIT_SUGGEST_MAX_LENGTH]

    suggested_keywords = _suggest_keywords(content)
    suggested_regexps  = _suggest_regexps(content) 
    suggested_tag_ids  = suggested_keywords | suggested_regexps

    # Turn the found IDs into tags 
    where_string = 'id IN (%s)' % ','.join(suggested_tag_ids)
    tags = Tag.objects.extra(where=[where_string])

    return tags
