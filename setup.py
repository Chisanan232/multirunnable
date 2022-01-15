import setuptools


with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="multirunnable",
    version="0.16.0",
    author="Liu, Bryant",
    author_email="chi10211201@cycu.org.tw",
    url="https://multirunnable.readthedocs.io",
    license="Apache License 2.0",
    description="A Python framework integrates running multiple tasks simultaneously with different strategy.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
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
    install_requires=[
        "gevent",
        "multipledispatch==0.6.0",
        "openpyxl==2.6.1"
    ]
)
