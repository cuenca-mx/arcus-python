from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'arcus/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='arcus',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Arcus API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/arcus-python',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.21,<2.28',
        'pytz>=2020.1,<2021.4',
        'iso8601>=0.1,<1.1',
        'pydash>=4.7,<5.2',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
