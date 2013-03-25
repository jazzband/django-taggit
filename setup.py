from setuptools import setup, find_packages


f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='django-taggit',
    version='0.10a1',
    description='django-taggit is a reusable Django application for simple tagging.',
    long_description=readme,
    author='Alex Gaynor',
    author_email='alex.gaynor@gmail.com',
    url='http://github.com/alex/django-taggit/tree/master',
    packages=find_packages(),
    package_data = {
        'taggit': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='taggit.tests.runtests.runtests',
    include_package_data=True,
    zip_safe=False,
)
