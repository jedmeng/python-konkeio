from setuptools import setup, find_packages


setup(
    name='pykonkeio',
    version='1.0.6',
    keywords=('konke', 'iot'),
    description='Python library for interfacing with konke smart appliances',
    long_description=open('README.rst', 'rt').read(),
    author='jedmeng',
    author_email='jedm@jedm.cn',
    url='https://github.com/jedmeng/python-konkeio',
    license='MIT',
    install_requires=[
        'pycryptodome>=3.6.0'
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
