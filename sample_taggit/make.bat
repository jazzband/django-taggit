:: make.bat

@echo off

set PYTHON=python
if not "%2" == "" (
    set PYTHON=%2
)

if "%1" == "reset-db" (
    %PYTHON% manage.py migrate library_management zero
    %PYTHON% manage.py migrate taggit zero
    %PYTHON% manage.py migrate
    for %%f in (fixtures\*.json) do (
        %PYTHON% manage.py loaddata %%f
    )
) else if "%1" == "export-data" (
    %PYTHON% manage.py dumpdata --indent 2 auth.User --output=fixtures\0001_users.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.Author --output=fixtures\0002_author.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.BookType --output=fixtures\0003_book_type.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.Book --output=fixtures\0004_books.json
    %PYTHON% manage.py dumpdata --indent 2 taggit.Tag --output=fixtures\0005_tags.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.ConditionTag --output=fixtures\0006_condition_tags.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.PhysicalCopy --output=fixtures\0007_tags.json
    %PYTHON% manage.py dumpdata --indent 2 library_management.ConditionTaggedItem --output=fixtures\0008_condition_tagged_item.json
) else if "%1" == "loaddata" (
    for %%f in (fixtures\*.json) do (
        %PYTHON% manage.py loaddata %%f
    )
) else (
    echo Invalid command. Use 'reset-db', 'export', or 'loaddata'.
)
