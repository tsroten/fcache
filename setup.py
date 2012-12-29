from distutils.core import setup

setup(
    name = "fcache",
    package_dir = {"": "lib"}
    py_modules = ["fcache"]
    version = "0.1",
    description = "A simple file-based cache.",
    author = "Thomas Roten",
    author_email = "thomas@roten.us",
    url = "http://github.com/tsroten",
    download_url = "",
    keywords = ["cache", "file"],
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        ],
    long_description = """

    """
)
