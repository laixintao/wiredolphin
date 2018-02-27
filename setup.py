# -*- coding: utf-8 -*-

from distutils.core import setup

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='wiredolphin',
    version='0.0.1',
    description='Network capture.',
    author='laixintao',
    author_email='laixintao1995@163.com',
    url='https://www.python.org/',
    packages=['wiredolphin'],
)
