#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setup file for the package"""

from setuptools import setup


def readme():
    """returns the content of the readme file"""
    with open('README.md') as rdme:
        return rdme.read()

setup(name='pyneo',
      version='0.2',
      description='Package to handle neo4j server connection',
      long_description=readme(),
      keywords='neo4j graph database',
      url='http://github.com/ArnaudParan/pyneo',
      author='Arnaud Paran',
      author_email='paran.arnaud@gmail.com',
      license='MIT',
      packages=['pyneo'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
