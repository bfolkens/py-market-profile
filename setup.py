from setuptools import setup
from setuptools import find_packages

import os

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='MarketProfile',
    version=version,
    author='Brad Folkens',
    author_email='bfolkens@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/bfolkens/py-market-profile',
    license='BSD license',
    description='A library to calculate Market Profile from a Pandas DataFrame.',
    long_description=open('README.rst').read(),
    install_requires=[
        "numpy >= 1.13.0",
        "pandas >= 0.20.3",
        "scipy >= 0.11.0"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords=['python', 'finance', 'quant', 'market profile', 'volume profile'],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development :: Libraries'
    ],
)
