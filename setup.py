import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

setup(
    name='django-cms-smartsnippets',
    version='0.1.2',
    description='Parametrizable Django CMS snippets.',
    long_description = open(README_PATH, 'r').read(),
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
)
