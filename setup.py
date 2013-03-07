import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

setup(
    name='django-cms-smartsnippets',
    version='0.1.13',
    description='Parametrizable Django CMS snippets.',
    long_description = open(README_PATH, 'r').read(),
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    setup_requires = ['s3sourceuploader', ],
    install_requires= ['django-cms==2.3.3', ],
    tests_require = ['django-nose', ],
    test_suite = 'runtests.runtests',
)
