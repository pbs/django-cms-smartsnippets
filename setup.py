import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

dependencies = [
    'django>=1.3,<1.5',
    'django-cms>=2.3,<2.3.6',
    'django-admin-extend'
]

dependency_links = [
    'http://github.com/pbs/django-admin-extend/tarball/master#egg=django-admin-extend-dev',
]


setup(
    name='django-cms-smartsnippets',
    version='0.4.0',
    description='Parametrizable Django CMS snippets.',
    long_description = open(README_PATH, 'r').read(),
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    install_requires=dependencies,
    dependency_links=dependency_links,
    setup_requires = ['s3sourceuploader', ],
)
