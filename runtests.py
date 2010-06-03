#!/usr/bin/env python

from os.path import dirname, abspath
import sys

from django.conf import settings as django_settings

if not django_settings.configured:
    django_settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'taggit',
            'taggit.tests',
        )
    )

def runtests(*test_args):
    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    from django.test.simple import run_tests
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
