import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

dependencies = [
    'django-cms==3.2.0',
    'django-sekizai>=0.6.1,<0.9.0',
    'django-admin-extend',
    'django-classy-tags<=0.6.2'
]

dependency_links = [
    'http://github.com/pbs/django-admin-extend/tarball/master#egg=django-admin-extend-dev',
]


setup(
    name='django-cms-smartsnippets',
    version='2.3.1',
    description='Parametrizable Django CMS snippets.',
    long_description=open(README_PATH, 'r').read(),
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    install_requires=dependencies,
    dependency_links=dependency_links,
)
