"""Setup script for aigoo"""

import setuptools
from codecs import open
import sys

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

with open("README.md", encoding="utf-8") as file:
    readme = file.read()


# This call to setup() does all the work
setuptools.setup(
    name="aigoo",
    version="0.0.2",
    description="Compiler error solution",
    # long_description=readme,
    # long_description_content_type="text/markdown",
    url="https://github.com/aditya612/dope",
    author="Aditya Agarwal",
    author_email="naveenagarwal123451@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    packages=["aigoo"],
    # packages=setuptools.find_packages(),
    include_package_data=True,

    entry_points={"console_scripts": ["aigoo = aigoo.aigoo:__main__"]},
    install_requires=["BeautifulSoup4", "requests",
                      "urllib3", "tk", "numpy", "pandas"],
    requires=["BeautifulSoup4", "requests",
              "urllib3", "tk", "numpy", "pandas"],
)
