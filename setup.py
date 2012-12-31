from distutils.core import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name = "fcache",
    version = "0.2",
    author = "Thomas Roten",
    author_email = "thomas@roten.us",
    url = "https://github.com/tsroten/fcache",
    description = "a simple, persistent, file-based cache module for Python",
    long_description = long_description,
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        ],
    keywords = ["cache", "file"],
    py_modules = ["fcache"],
    test_suite = "test",
    install_requires = "appdirs",
)
