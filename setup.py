#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]


setup(
    author="Rick McGeer",
    author_email='rick@mcgeer.com',
    python_requires='>=3.6',
    classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Data Scientists',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License', 
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
    description="A Python implementation of the Simple Data Transfer Protocol data structures, function, server, and client",
    # install_requires=requirements,
    install_requires=[
        'Flask',
        'Flask-CORS',
        'numpy',
        'pandas',
        'requests',
        'Werkzeug'
    ],
    license="'BSD-3-Clause",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords = ['Data access', 'Data analytics'], 
    name='sdtp',
    packages=['sdtp'],
    # test_suite='tests',
    # tests_require=test_requirements,
    url='https://github.com/engageLively/sdtp',
    download_url = 'https://github.com/engagelLively/sdtp/archive/v_01.tar.gz',
    version='0.1.0',
    zip_safe=False,
)
