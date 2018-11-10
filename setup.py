#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pykonkeio',
    version='2.1.5',
    keywords=['konke', 'iot'],
    description='Python library for interfacing with konke smart appliances',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='jedmeng',
    author_email='jedm@jedm.cn',
    url='https://github.com/jedmeng/python-konkeio',
    license='GPLv3',
    install_requires=[
        'pycryptodome>=3.6.0'
    ],
    packages=find_packages(include=['pykonkeio', 'pykonkeio.*']),
    include_package_data=True,
    python_requires='>=3.5',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'konkeio = pykonkeio.__main__:main',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
