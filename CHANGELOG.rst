Changelog
=========

(Unreleased)
~~~~~~~~~~~~

* (nothing here yet)

1.4.0 (2021-04-19)
~~~~~~~~~~~~~~~~~~

* Add Python 3.9 support.
* Remove Python 3.5 support.
* Add Django 3.2 support.
* Remove Django 1.11 and 3.0 support.
* Add Danish translation.
* Fix crashing that could occur with ``similar_objects`` in multi-inheritance contexts.
* Add support for custom fields on through table models with `through_defaults` for ``TaggedManager.add`` and ``TaggedManager.set``.


1.3.0 (2020-05-19)
~~~~~~~~~~~~~~~~~~

* Model and field ``verbose_name`` and ``verbose_name_plural`` attributes are
  now lowercase. This simplifies using the name in the middle of a sentence.
  When used as a header, title, or at the beginning of a sentence, a text
  transformed can be used to adjust the case.
* Fix prefetch_related when using UUIDTaggedItem.
* Allow for passing in extra constructor parameters when using
  ``TaggableManager.add``. This is especially useful when using custom
  tag models.

1.2.0 (2019-12-03)
~~~~~~~~~~~~~~~~~~

* **Removed** support for end-of-life Django 2.0 and 2.1.
* Added support for Django 3.0.
* Added support for Python 3.8.
* Moved ``TaggedItemBase.tags_for()`` to ItemBase.
* Replaced reference to removed Django's ``.virtual_fields`` with
  ``.private_field``.
* Added ``TextareaTagWidget``.

1.1.0 (2019-03-22)
~~~~~~~~~~~~~~~~~~

* Added Finnish translation.
* Updated Chinese translation.
* Updated Esperanto translation.
* Fix ``form.changed_data`` to allow early access for a tags defined with
  ``blank=True``.

1.0.0 (2019-03-17)
~~~~~~~~~~~~~~~~~~

* **Backwards incompatible:** Remove support for Python 2.
* Added ``has_changed()`` method to ``taggit.forms.TagField``.
* Added multi-column unique constraint to model ``TaggedItem`` on fields
  ``content_type``, ``object_id``, and ``tag``. Databases that contain
  duplicates will need to add a data migration to resolve these duplicates.
* Fixed ``TaggableManager.most_common()`` to always evaluate lazily. Allows
  placing a ``.most_common()`` query at the top level of a module.
* Fixed setting the ``related_name`` on a tags manager that exists on a model
  named ``Name``.

0.24.0 (2019-02-19)
~~~~~~~~~~~~~~~~~~~

* The project has moved to `Jazzband <https://jazzband.co/>`_. This is the
  first release under the new organization. The new repository URL is
  `<https://github.com/jazzband/django-taggit>`_.
* Added support for Django 2.2.
* Fixed a race condition in ``TaggableManager``.
* Removed method ``ItemBase.bulk_lookup_kwargs()``.
* Fixed view ``tagged_object_list`` to set ``queryset.model`` as
  ``ListView.model`` (was previously set as a ``ContentType`` instance).
* ``_TaggableManager`` and ``TaggableManager`` now always call the parent
  class ``__init__``.
* Removed ``TaggableRel`` and replaced uses with ``ManyToManyRel``.

0.23.0 (2018-08-07)
~~~~~~~~~~~~~~~~~~~

* **Backwards incompatible:** Remove support for Django < 1.11
* Added support for Django 2.1 and Python 3.7
* Moved TagWidget value conversion from TagWidget.render() to TagWidget.format_value()

0.22.2 (2017-12-27)
~~~~~~~~~~~~~~~~~~~

* Added support for Django 2.0
* **Backwards incompatible:** Dropped support for EOL Python 3.3

0.22.1 (2017-04-22)
~~~~~~~~~~~~~~~~~~~

* Update spanish translation
* Add testing for Django 1.11 and Python 3.6
* introduce isort and flake8 in the CI
* [docs] Fixed links to external apps
* Improved auto-slug in TagBase to support UUID pk
* [docs] Added contribution guidelines

0.22.0 (2017-01-29)
~~~~~~~~~~~~~~~~~~~

* **Backwards incompatible:** Drop support for Django 1.7

0.21.6 (2017-01-25)
~~~~~~~~~~~~~~~~~~~

* Fix case-insensitive tag creation when setting to a mix of new and existing
  tags are used

0.21.5 (2017-01-21)
~~~~~~~~~~~~~~~~~~~

* Check for case-insensitive duplicates when creating new tags

0.21.4 (2017-01-10)
~~~~~~~~~~~~~~~~~~~

* Support __gt__ and __lt__ ordering on Tags

0.21.3 (2016-10-07)
~~~~~~~~~~~~~~~~~~~

* Fix list view

0.21.2 (2016-08-31)
~~~~~~~~~~~~~~~~~~~

* Update Python version classifiers in setup.py
* Add Greek translation

0.21.1 (2016-08-25)
~~~~~~~~~~~~~~~~~~~

* Document supported versions of Django; fix Travis to test these versions.

0.21.0 (2016-08-22)
~~~~~~~~~~~~~~~~~~~

* Fix form tests on Django 1.10
* Address list_display and fieldsets in admin docs
* external_apps.txt improvements
* Remove support for Django 1.4-1.6, again.

0.20.2 (2016-07-11)
~~~~~~~~~~~~~~~~~~~

* Add extra_filters argument to the manager's most_common method

0.20.1 (2016-06-23)
~~~~~~~~~~~~~~~~~~~

* Specify `app_label` for `Tag` and `TaggedItem`

0.20.0 (2016-06-19)
~~~~~~~~~~~~~~~~~~~

* Fix UnboundLocalError in _TaggableManager.set(..)
* Update doc links to reflect RTD domain changes
* Improve Russian translations

0.19.1 (2016-05-25)
~~~~~~~~~~~~~~~~~~~

* Add app config, add simplified Chinese translation file

0.19.0 (2016-05-23)
~~~~~~~~~~~~~~~~~~~

* Implementation of m2m_changed signal sending
* Code and tooling improvements

0.18.3 (2016-05-12)
~~~~~~~~~~~~~~~~~~~

* Added Spanish and Turkish translations

0.18.2 (2016-05-08)
~~~~~~~~~~~~~~~~~~~

* Add the min_count parameter to managers.most_common function

0.18.1 (2016-03-30)
~~~~~~~~~~~~~~~~~~~

* Address deprecation warnings

0.18.0 (2016-01-18)
~~~~~~~~~~~~~~~~~~~

* Add option to override default tag string parsing
* Drop support for Python 2.6

0.17.6 (2015-12-09)
~~~~~~~~~~~~~~~~~~~

* Silence Django 1.9 warning

0.17.5 (2015-11-27)
~~~~~~~~~~~~~~~~~~~

* Django 1.9 compatibility fix

0.17.4 (2015-11-25)
~~~~~~~~~~~~~~~~~~~

* Allows custom Through Model with GenericForeignKey

0.17.3 (2015-10-26)
~~~~~~~~~~~~~~~~~~~

* Silence Django 1.9 warning about on_delete

0.17.2 (2015-10-25)
~~~~~~~~~~~~~~~~~~~

* Django 1.9 beta compatibility

0.17.1 (2015-09-10)
~~~~~~~~~~~~~~~~~~~

* Fix unknown column `object_id` issue with Django 1.6+

0.17.0 (2015-08-14)
~~~~~~~~~~~~~~~~~~~

* Database index added on TaggedItem fields content_type & object_id

0.16.4 (2015-08-13)
~~~~~~~~~~~~~~~~~~~

* Access default manager via class instead of instance

0.16.3 (2015-08-08)
~~~~~~~~~~~~~~~~~~~

* Prevent IntegrityError with custom TagBase classes

0.16.2 (2015-07-13)
~~~~~~~~~~~~~~~~~~~

* Fix an admin bug related to the `Manager` property `through_fields`

0.16.1 (2015-07-09)
~~~~~~~~~~~~~~~~~~~

* Fix bug that assumed all primary keys are named 'id'

0.16.0 (2015-07-04)
~~~~~~~~~~~~~~~~~~~

* Add option to allow case-insensitive tags

0.15.0 (2015-06-23)
~~~~~~~~~~~~~~~~~~~

* Fix wrong slugs for non-latin chars. Only works if optional GPL dependency
  (unidecode) is installed.

0.14.0 (2015-04-26)
~~~~~~~~~~~~~~~~~~~

* Prevent extra JOIN when prefetching
* Prevent _meta warnings with Django 1.8

0.13.0 (2015-04-02)
~~~~~~~~~~~~~~~~~~~

* Django 1.8 support

0.12.3 (2015-03-03)
~~~~~~~~~~~~~~~~~~~

* Specify that the internal type of the TaggitManager is a ManyToManyField

0.12.2 (2014-21-09)
~~~~~~~~~~~~~~~~~~~

* Fixed 1.7 migrations.

0.12.1 (2014-10-08)
~~~~~~~~~~~~~~~~~~~

* Final (hopefully) fixes for the upcoming Django 1.7 release.
* Added Japanese translation.

0.12.0 (2014-20-04)
~~~~~~~~~~~~~~~~~~~

* **Backwards incompatible:** Support for Django 1.7 migrations. South users
  have to set ``SOUTH_MIGRATION_MODULES`` to use ``taggit.south_migrations``
  for taggit.
* **Backwards incompatible:** Django's new transaction handling is used on
  Django 1.6 and newer.
* **Backwards incompatible:** ``Tag.save`` got changed to opportunistically try
  to save the tag and if that fails fall back to selecting existing similar
  tags and retry -- if that fails too an ``IntegrityError`` is raised by the
  database, your app will have to handle that.
* Added Italian and Esperanto translations.

0.11.2 (2013-13-12)
~~~~~~~~~~~~~~~~~~~

* Forbid multiple TaggableManagers via generic foreign keys.

0.11.1 (2013-25-11)
~~~~~~~~~~~~~~~~~~~

* Fixed support for Django 1.4 and 1.5.

0.11.0 (2013-25-11)
~~~~~~~~~~~~~~~~~~~

* Added support for prefetch_related on tags fields.
* Fixed support for Django 1.7.
* Made the tagging relations unserializeable again.
* Allow more than one TaggableManager on models (assuming concrete FKs are
   used for the relations).

0.10.0 (2013-17-08)
~~~~~~~~~~~~~~~~~~~

* Support for Django 1.6 and 1.7.
* Python3 support
* **Backwards incompatible:** Dropped support for Django < 1.4.5.
* Tag names are unique now, use the provided South migrations to upgrade.

0.9.2 (2011-01-17)
~~~~~~~~~~~~~~~~~~

* **Backwards incompatible:** Forms containing a :class:`TaggableManager` by
  default now require tags, to change this provide ``blank=True`` to the
  :class:`TaggableManager`.
* Now works with Django 1.3 (as of beta-1).

0.9.0 (2010-09-22)
~~~~~~~~~~~~~~~~~~

* Added a Hebrew locale.
* Added an index on the ``object_id`` field of ``TaggedItem``.
* When displaying tags always join them with commas, never spaces.
* The docs are now available `online <https://django-taggit.readthedocs.io/>`_.
* Custom ``Tag`` models are now allowed.
* **Backwards incompatible:** Filtering on tags is no longer
  ``filter(tags__in=["foo"])``, it is written
  ``filter(tags__name__in=["foo"])``.
* Added a German locale.
* Added a Dutch locale.
* Removed ``taggit.contrib.suggest``, it now lives in an external application,
   see :doc:`external_apps` for more information.

0.8.0 (2010-06-22)
~~~~~~~~~~~~~~~~~~

* Fixed querying for objects using ``exclude(tags__in=tags)``.
* Marked strings as translatable.
* Added a Russian translation.
* Created a `mailing list <http://groups.google.com/group/django-taggit>`_.
* Smarter tagstring parsing for form field; ported from Jonathan Buchanan's
  `django-tagging <http://django-tagging.googlecode.com>`_. Now supports tags
  containing commas. See :ref:`tags-in-forms` for details.
* Switched to using savepoints around the slug generation for tags. This
  ensures that it works fine on databases (such as Postgres) which dirty a
  transaction with an ``IntegrityError``.
* Added Python 2.4 compatibility.
* Added Django 1.1 compatibility.
