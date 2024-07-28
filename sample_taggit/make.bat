:: make.bat

@echo off

if "%1" == "reset" (
    python manage.py migrate library_management zero
    del library_management\migrations\0001_initial.py
    python manage.py makemigrations library_management
    python manage.py migrate
    for %%f in (fixtures\*.json) do (
        python manage.py loaddata %%f
    )
) else if "%1" == "install" (
    pip install -r requirements.txt
) else if "%1" == "clean" (
    rmdir /s /q __pycache__
    
) else if "%1" == "export" (
    python manage.py dumpdata --indent 2 auth.User --output=fixtures\0001_users.json
    python manage.py dumpdata --indent 2 library_management.Author --output=fixtures\0002_author.json
    python manage.py dumpdata --indent 2 library_management.BookType --output=fixtures\0003_book_type.json
    python manage.py dumpdata --indent 2 library_management.Book --output=fixtures\0004_books.json
    python manage.py dumpdata --indent 2 taggit.Tag --output=fixtures\0005_tags.json
    python manage.py dumpdata --indent 2 library_management.ConditionTag --output=fixtures\0006_condition_tags.json
    python manage.py dumpdata --indent 2 library_management.PhysicalCopy --output=fixtures\0007_tags.json
    python manage.py dumpdata --indent 2 library_management.ConditionTaggedItem --output=fixtures\0008_condition_tagged_item.json
) else (
    echo Invalid command. Use 'reset', 'install', 'clean', or 'export'.
)