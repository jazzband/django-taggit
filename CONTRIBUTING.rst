Contributing to django-taggit
=============================

.. image:: https://jazzband.co/static/img/jazzband.svg
   :target: https://jazzband.co/
   :alt: Jazzband

This is a `Jazzband <https://jazzband.co>`_ project. By contributing you agree
to abide by the `Contributor Code of Conduct
<https://jazzband.co/about/conduct>`_ and follow the `guidelines
<https://jazzband.co/about/guidelines>`_.

Thank you for taking the time to contribute to django-taggit.

Follow these guidelines to speed up the process.

Reach out before you start
--------------------------

Before opening a new issue, look if somebody else has already started working
on the same issue in the `GitHub issues
<https://github.com/jazzband/django-taggit/issues>`_ and `pull requests
<https://github.com/jazzband/django-taggit/pulls>`_.

Fork the repository
-------------------

Once you have forked this repository to your own GitHub account, install your
own fork in your development environment:

.. code-block:: console

    git clone git@github.com:<your_fork>/django-taggit.git
    cd django-taggit
    python setup.py develop

Running tests
-------------

django-taggit uses `tox <https://tox.readthedocs.io/>`_ to run tests:

.. code-block:: console

    tox

Follow style conventions (black, flake8, isort)
-----------------------------------------------

Check that your changes are not breaking the style conventions with:

.. code-block:: console

    tox -e black,flake8,isort

Update the documentation
------------------------

If you introduce new features or change existing documented behavior, please
remember to update the documentation.

The documentation is located in the ``docs`` directory of the repository.

To do work on the docs, proceed with the following steps:

.. code-block:: console

    pip install sphinx
    sphinx-build -n -W docs docs/_build

Send pull request
-----------------

It is now time to push your changes to GitHub and open a `pull request
<https://github.com/jazzband/django-taggit/pulls>`_!


Release Checklist
-----------------

To make a release, the following needs to happen:

- Bump the version number in ``taggit/__init__.py``
- Update the changelog (making sure to add the (Unreleased) section to the top)
- Get those changes onto the ``master`` branch
- Tag the commit with the version number
- CI should then upload a release to be verified through Jazzband
