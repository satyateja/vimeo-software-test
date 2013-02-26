#!/usr/bin/env python

from setuptools import setup

setup(
    name='Vimeo',
    version='1.0',
    description='OpenShift App',
    author='Satya Teja',
    author_email='satyateja999@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    # Your 3part apps:
    install_requires=['Django==1.4.2', 'python-memcached==1.48', 'simplejson==2.6.1', 'distribute==0.6.28',
                      'mysql-python', 'requests==0.14.0'],
    )
