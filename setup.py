import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args or '')
        sys.exit(errno)

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

version = '0.2dev'

# read long description from README
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    packages=packages,
    name='pandana',
    author='Autodesk',
    version=version,
    license='AGPL',
    description=('Pandas Network Analysis - '
                 'dataframes of network queries, quickly'),
    long_description=long_description,
    url='https://udst.github.io/pandana/',
    setup_requires=['cffi >= 1.1'],
    cffi_modules=['pandana/accesswrap_build.py:ffi'],
    install_requires=[
        'cffi >= 1.1',
        'matplotlib>=1.3.1',
        'numpy>=1.8.0',
        'pandas>=0.13.1',
        'requests>=2.0',
        'tables>=3.1.0'
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
)
