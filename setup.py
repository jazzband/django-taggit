from setuptools import find_packages, setup

import taggit

with open('README.rst') as f:
    readme = f.read()

setup(
    name='django-taggit',
    version='.'.join(str(i) for i in taggit.VERSION),
    description='django-taggit is a reusable Django application for simple tagging.',
    long_description=readme,
    author='Alex Gaynor',
    author_email='alex.gaynor@gmail.com',
    url='http://github.com/alex/django-taggit/tree/master',
    packages=find_packages(exclude=('tests*',)),
    package_data={
        'taggit': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'isort'
    ],
)
