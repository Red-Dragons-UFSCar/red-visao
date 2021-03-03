import os
from setuptools import find_packages, setup

with open('README.md') as fh:
    readme = fh.read()
with open('requirements.txt') as fh:
    req = fh.read()

setup(
    name = 'reddragons',
    version = '1.0.1',
    author = 'Red Dragons',
    description = 'Repositório contendo o código de 2020 utilizado pela equipe Red Dragons',
    packages = find_packages(),
    long_description = readme
)