#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        DATABASES = {
            'default': {'ENGINE': 'django.db.backends.sqlite3'}
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'taggit',
            'taggit.tests',
        ]
    )

from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args):
    if not test_args:
        test_args = ['tests']
    parent = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
    )
    sys.path.insert(0, parent)
    runner = DjangoTestSuiteRunner()
    failures = runner.run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
