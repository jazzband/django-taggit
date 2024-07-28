# Makefile

reset-db:
    python manage.py migrate zero;
    python manage.py migrate;
    python manage.py loaddata library_management/fixtures/*.json
