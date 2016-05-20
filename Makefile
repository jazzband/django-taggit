.PHONY: develop test

develop:
	pip install -q -r requirements/test.txt
	pip install -q -e .

test: develop
	DJANGO_SETTINGS_MODULE=tests.settings py.test tests/tests.py --cov=taggit
