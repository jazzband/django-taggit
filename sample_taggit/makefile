# Makefile

PYTHON ?= python3

reset-db:
	$(PYTHON) manage.py migrate library_management zero;
	$(PYTHON) manage.py migrate taggit zero;
	$(PYTHON) manage.py migrate;
	$(PYTHON) manage.py loaddata fixtures/*.json

export-data:
	$(PYTHON) manage.py dumpdata --indent 2 auth.User --output=sample_taggit/fixtures/0001_users.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.Author --output=sample_taggit/fixtures/0002_author.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.BookType --output=sample_taggit/fixtures/0003_book_type.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.Book --output=sample_taggit/fixtures/0004_books.json;
	$(PYTHON) manage.py dumpdata --indent 2 taggit.Tag --output=sample_taggit/fixtures/0005_tags.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.ConditionTag --output=sample_taggit/fixtures/0006_condition_tags.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.PhysicalCopy --output=sample_taggit/fixtures/0007_tags.json;
	$(PYTHON) manage.py dumpdata --indent 2 library_management.ConditionTaggedItem --output=sample_taggit/fixtures/0008_condition_tagged_item.json;

loaddata:
	$(PYTHON) manage.py loaddata fixtures/*.json
