.PHONY: develop test

develop:
	pip install -q -r requirements/test.txt

test:
	DJANGO_SETTINGS_MODULE=tests.settings py.test tests/tests.py --cov=taggit
