#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name='pykonkeio',
    version='2.0.1b0',
    keywords=['konke', 'iot'],
    description='Python library for interfacing with konke smart appliances',
    long_description=open('README.md', 'rt').read(),
    author='jedmeng',
    author_email='jedm@jedm.cn',
    url='https://github.com/jedmeng/python-konkeio',
    license='GPLv3',
    install_requires=[
        'pycryptodome>=3.6.0'
    ],
    packages=find_packages(exclude=['tests', 'tests.*', 'mock', 'mock.*']),
    include_package_data=True,
    python_requires='>=3.5',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'konkeio = pykonkeio.__main__:main',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
)
