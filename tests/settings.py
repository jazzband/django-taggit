import os

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

# Templates
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(
    os.path.abspath(
        os.path.join(SETTINGS_DIR, os.path.pardir),
    ),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(ROOT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]
