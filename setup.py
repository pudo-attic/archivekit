from setuptools import setup, find_packages

setup(
    name='barn',
    version='0.0.1',
    description="Store a set of files and metadata in an organized way",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://pudo.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Werkzeug>=0.9.6",
        "lockfile>=0.9.1",
        "python-slugify>=0.0.6",
        "boto>=2.33",
        "moto>=0.3.9",
        "nose>=1.3.0"
    ],
    entry_points={
        'barn.stores': [
            's3 = barn.store.s3:S3Store',
            'file = barn.store.file:FileStore'
        ],
        'barn.resource_types': [
            'source = barn.types.source:Source'
        ],
        #'console_scripts': [
        #    'barn = barn.cli:cli'
        #]
    },
    tests_require=[
    ]
)
