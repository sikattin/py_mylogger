# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mylogger',
    version='1.2',
    description='logger module.',
    long_description='logger module',
    author='Takeki Shikano',
    author_email='shikano.takeki@nexon.co.jp',
    url=None,
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
)

