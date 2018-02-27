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
    install_requires=requirements,
    dependency_links=[
        "https://github.com/tonycpsu/panwid/tarball/master#egg=panwid-0.2.0dev",
        "https://github.com/laixintao/py3shark/tarball/master#egg=pyshark-0.4.0",
    ]
)
