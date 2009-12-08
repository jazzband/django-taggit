from setuptools import setup, find_packages

f = open('README.txt')
readme = f.read()
f.close()

setup(
    name='django-taggit',
    version='0.1-pre',
    description='django-taggit is a reusable Django application for simple tagging.',
    long_description=readme,
    author='Alex Gaynor',
    author_email='alex.gaynor@gmail.com',
    url='http://github.com/alex/django-taggit/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

