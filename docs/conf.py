extensions = ["sphinx.ext.intersphinx"]

master_doc = "index"

project = "django-taggit"
copyright = "Alex Gaynor and individual contributors."

# The short X.Y version.
version = "1.3"
# The full version, including alpha/beta/rc tags.
release = "1.3.0"

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
}
