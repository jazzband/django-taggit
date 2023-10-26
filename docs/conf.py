import taggit

extensions = ["sphinx.ext.intersphinx"]

master_doc = "index"

project = "django-taggit"
copyright = "Alex Gaynor and individual contributors."

# The short X.Y version.
version = taggit.__version__
# The full version, including alpha/beta/rc tags.
release = taggit.__version__

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
}
