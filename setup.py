from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'arcus/version.py').load_module()

test_requires = [
    'pytest==5.4.3',
    'pytest-vcr==1.0.2',
    'pytest-cov==2.10.0',
    'black==19.10b0',
    'isort==5.0.*',
    'flake8==3.8.1',
    'mypy==0.782',
    'requests-mock==1.8.0',
]

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
        'requests==2.21.0',
        'pytz==2020.1',
        'iso8601==0.1.12',
        'pydash==4.7.4',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
