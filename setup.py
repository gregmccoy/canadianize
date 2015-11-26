from setuptools import setup, find_packages
import os

setup(
    name = 'versebg',
    author = "Greg McCoy",
    author_email = "gregmccoy@gfa.org",
    url = "",
    version = '0.1.0',
    packages=['ca'],
    package_dir={'ca': 'src/ca'},
    package_data={'ca': 'data/*'},
    scripts=['ca'],
    license='Open Source!',
    long_description=open('README.md').read(),

    install_requires = ['enchant', 'html2text']
    )