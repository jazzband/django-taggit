from django import VERSION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'taggit',
    'tests',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]

if VERSION <= (1, 9):
    MIDDLEWARE_CLASSES = []
else:
    MIDDLEWARE = []

SECRET_KEY = 'secretkey'
