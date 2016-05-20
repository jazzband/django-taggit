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

MIDDLEWARE_CLASSES = []

SECRET_KEY = 'secretkey'
