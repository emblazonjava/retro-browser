#!/usr/bin/env python

from distutils.core import setup

setup(name='RetroBrowser',
      version='0.1',
      description='A Python implementation of a text-based Grails',
      author='Allison F',
      author_email='yetanotherallisonf@yahoo.com',
      url='https://github.com/allisonf/retro-browser',
      packages=['retrobrowser.framework',
                'retrobrowser.framework.defaultapp',
                'retrobrowser.framework.defaultapp.controllers',
                'retrobrowser.framework.defaultapp.views.Error400',
                'retrobrowser.framework.defaultapp.views.Error404',
                'retrobrowser.framework.defaultapp.views.Error500'],
      scripts=[
          'bin/retroBrowser'
      ]
     )
