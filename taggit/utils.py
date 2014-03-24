from __future__ import unicode_literals

import re

from django.conf import settings

from django.utils.encoding import force_text
from django.utils.functional import wraps


# Regular expression that will split tag on spaces, except when the tag is
# surrounded by quotation marks.
DEFAULT_TAG_DELIMITER = r"(?: |\"(.*?)\"|'.*?'),?"
TAG_DELIMITER = getattr(settings, 'TAGGIT_TAG_DELIMITER',
                        DEFAULT_TAG_DELIMITER)
TAG_SEPARATOR = getattr(settings, 'TAGGIT_TAG_SEPARATOR', ', ')


def parse_tags(tagstring, tag_delimiter=TAG_DELIMITER):
    """
    Parses tag input, with default behavior of multiple word input being
    activated and delineated by commas and double quotes. Quotes take
    precedence, so they may contain commas.

    Returns a sorted list of unique tag names.

    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """
    if not tagstring:
        return []

    tagstring = force_text(tagstring)

    # The default regex pattern will return each whitespace as a token, so we
    # need to discard all whitespace tokens, keeping only the  as a
    splitter = re.compile(TAG_DELIMITER)
    words = set(w for w in splitter.split(tagstring) if w)
    words = list(words)
    words.sort()
    return words


def split_strip(string, delimiter=TAG_DELIMITER):
    """
    Splits ``string`` on ``delimiter``, stripping each resulting string
    and returning a list of non-empty strings.

    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """
    if not string:
        return []

    words = [w.strip() for w in string.split(delimiter)]
    return [w for w in words if w]


def edit_string_for_tags(tags):
    """
    Given list of ``Tag`` instances, creates a string representation of
    the list suitable for editing by the user, such that submitting the
    given string representation back without changing it will give the
    same list of tags.

    Tag names which contain commas will be double quoted.

    If any tag name which isn't being quoted contains whitespace, the
    resulting string of tag names will be comma-delimited, otherwise
    it will be space-delimited.

    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """
    names = []
    for tag in tags:
        name = tag.name
        if TAG_DELIMITER in name:
            names.append('"%s"' % name)
        else:
            names.append(name)
    return TAG_SEPARATOR.join(sorted(names))


def require_instance_manager(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
        return func(self, *args, **kwargs)
    return inner
