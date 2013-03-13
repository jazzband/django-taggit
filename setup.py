from setuptools import setup, find_packages

from taggit import VERSION


f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='django-taggit',
    version=".".join(map(str, VERSION)),
    description='django-taggit is a reusable Django application for simple tagging.',
    long_description=readme,
    author='Alex Gaynor',
    author_email='alex.gaynor@gmail.com',
    url='http://github.com/alex/django-taggit/tree/master',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        'taggit': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='taggit.tests.runtests.runtests',
)
