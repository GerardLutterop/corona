# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='okapi.framework',
    version='0.8',
    packages=find_packages(include=('yourapi.*',)),
    url='https://github.com/yourapi/okapi.framework',
    license='',
    author='Leonard de Vries',
    author_email='leonard.devries@bizservices.nl',
    description='Framework for running yourapi service and loading plugins.',
    install_requires=required,
    include_package_data=True
)
