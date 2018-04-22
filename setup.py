from setuptools import setup, find_packages


setup(
    name='pykonkeio',
    version='1.0.2',
    keywords=('konke', 'iot'),
    description='Python library for interfacing with konke smart appliances',
    long_description=open('README.md', 'rt').read(),
    author='jedmeng',
    author_email='jedm@jedm.cn',
    url='https://github.com/jedmeng/python-konkeio',
    license='MIT',
    install_requires=[
        'pycrypto'
    ],
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.5',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'konkeio=pykonkeio.__main__:main',
        ]
    },
)
