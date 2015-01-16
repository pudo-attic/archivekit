import os
from setuptools import setup, find_packages

setup(
    name='docstash',
    version='0.2.2',
    description="Store a set of documents and metadata in an organized way",
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
        "PyYAML>=3.11",
        "Werkzeug>=0.9.6",
        "lockfile>=0.9.1"
    ],
    entry_points={},
    tests_require=[]
)
