import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='arcus',
    version='0.0.2',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Arcus API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/arcus-python',
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': [
            'pytest>=3',
            'pycodestyle'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
