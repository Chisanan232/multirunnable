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
        "Programming Language :: Python",
        "License :: OSI Approved :: APACHE-2.0 License",
        "Operating System :: OS Independent",
        "Topic :: Parallel/Engineering",
        "Topic :: Concurrent/Engineering",
        "Topic :: Coroutine/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
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
