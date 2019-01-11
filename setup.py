import setuptools

install_requirements = [
    'requests==2.21.0',
    'pytz==2018.9',
    'iso8601==0.1.12',
    'pydash==4.7.4'
]

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='arcus',
    version='0.2.6',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Arcus API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/arcus-python',
    packages=setuptools.find_packages(),
    install_requires=install_requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'vcrpy'],
    extras_require={
        'dev': [
            'pytest>=3',
            'pycodestyle',
            'coverage'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
