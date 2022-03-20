import setuptools
import os


here = os.path.abspath(os.path.dirname(__file__))

packages = ["multirunnable"]

requires = [
    "gevent",
    "multipledispatch>=0.6.0",
    "openpyxl>=2.6.1"
]

test_requires = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "pytest-html>=3.1.1",
    "pytest-rerunfailures>=10.2",
    "codecov>=2.1.12",
    "coveralls>=3.3.1"
]


about = {}
with open(os.path.join(here, "multirunnable", "__pkg_info__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)


with open("README.md", "r") as fh:
    readme = fh.read()


setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=packages,
    package_dir={"multirunnable": "multirunnable"},
    py_modules=packages,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keyword="multirunnable parallel concurrent coroutine",
    python_requires='>=3.6',
    install_requires=requires,
    tests_require=test_requires,
    project_urls={
        "Documentation": "https://multirunnable.readthedocs.io",
        "Source": "https://github.com/Chisanan232/multirunnable",
    },
)
