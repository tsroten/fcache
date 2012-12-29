from distutils.core import setup

setup(
    name = "fcache",
    py_modules = ["fcache"],
    test_suite = "test",
    install_requires = "appdirs",
    version = "0.1",
    description = "A simple file-based cache module for Python",
    author = "Thomas Roten",
    author_email = "thomas@roten.us",
    url = "https://github.com/tsroten/fcache",
    keywords = ["cache", "file"],
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        ],
    long_description = open('README.rst').read(),
)
