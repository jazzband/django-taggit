import re

from django.conf import settings

from taggit.contrib.suggest.models import TagKeyword, TagRegex
from taggit.models import Tag


def _suggest_keywords(content):
    """ Suggest by keywords """
    suggested_keywords = set()
    keywords = TagKeyword.objects.all()

    for k in keywords:
        # Use the stem if available, otherwise use the whole keyword
        if k.stem:
            if k.stem in content:
                suggested_keywords.add(k.tag_id)
        elif k.keyword in content:
            suggested_keywords.add(k.tag_id)

    return suggested_keywords

def _suggest_regexes(content):
    """ Suggest by regular expressions """
    # Grab all regular expressions and compile them
    suggested_regexes = set()
    regex_keywords = TagRegex.objects.all()

    # Look for our regular expressions in the content
    for r in regex_keywords:
        if re.search(r.regex, content):
            suggested_regexes.add(r.tag_id)

    return suggested_regexes

def suggest_tags(content):
    """ Suggest tags based on text content """
    suggested_keywords = _suggest_keywords(content)
    suggested_regexes  = _suggest_regexes(content)
    suggested_tag_ids  = suggested_keywords | suggested_regexes

    return Tag.objects.filter(id__in=suggested_tag_ids)
