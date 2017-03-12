from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='fcache',
    version='0.4.7',
    author='Thomas Roten',
    author_email='thomas@roten.us',
    url='https://github.com/tsroten/fcache',
    description='a dictionary-like, file-based cache module for Python',
    long_description=long_description,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Filesystems',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['cache', 'file', 'serialize'],
    packages=['fcache', 'tests'],
    test_suite='tests',
    install_requires=['appdirs'],
)
