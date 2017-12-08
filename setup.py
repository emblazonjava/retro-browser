#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='RetroBrowser',
    version='0.1',
    description='A Python implementation of a text-based Grails',
    author='Allison F',
    author_email='yetanotherallisonf@yahoo.com',
    url='https://github.com/allisonf/retro-browser',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Terminals',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='mvc command line text based games',

    packages=find_packages(exclude=['docs', 'tests']),

    scripts=[
      'bin/retroBrowser'
    ],
    install_requires=["ConventionCrawler"]
)
