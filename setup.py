import os
from setuptools import setup, find_packages

VERSION = '0.0.1'
PKG_NAME = 'wls'
URL = 'https://github.com/aharol/wls.git'

setup(
    name=PKG_NAME,
    version=VERSION,
    packages=find_packages(),
    package_dir={PKG_NAME: PKG_NAME},
    include_package_data=True,
    author='Art Harol',
    license="Apache Licence 2.0",
    url=URL,
    description='See %s' % URL,
    test_suite='%s.tests' % PKG_NAME,
)
