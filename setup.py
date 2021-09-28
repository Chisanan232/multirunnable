import setuptools


with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="multirunnable",
    version="0.15.0",
    author="Liu, Bryant",
    author_email="chi10211201@cycu.org.tw",
    description="A Python framework integrates running multiple tasks simultaneously with different strategy.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        # "Topic :: Build MultiRunnable Programming",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keyword="multirunnable parallel concurrent coroutine",
    python_requires='>=3.6',
    install_requires=[
        "gevent==1.4.0",
        "multipledispatch==0.6.0",
        "colorama==0.4.1",
        "kafka-python==2.0.2",
        "openpyxl==2.6.1",
        "deprecated==1.2.11"
    ]
)
