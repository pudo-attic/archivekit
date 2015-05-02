from setuptools import setup, find_packages

setup(
    name='archivekit',
    version='0.5.3',
    description="Store a set of files and metadata in an organized way",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='storage filesystem archive bagit bag etl data processing',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://pudo.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        "Werkzeug>=0.9.6",
        "lockfile>=0.9.1",
        "python-slugify>=0.0.6",
        "requests>=2.2.0",
        "boto>=2.33",
        "six"
    ],
    entry_points={
        'archivekit.stores': [
            's3 = archivekit.store.s3:S3Store',
            'file = archivekit.store.file:FileStore'
        ],
        'archivekit.resource_types': [
            'source = archivekit.types.source:Source'
        ],
    },
    tests_require=[]
)
