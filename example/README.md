# Example Code with '_multirunnable_'

Here are some example code about how to use this package.

[comment]: <> ([Environment]&#40;#environment&#41; | [Simple]&#40;#simple&#41; | [Persistence]&#40;#persistence&#41;)

## Environment
<hr>

[![Supported Versions](https://img.shields.io/pypi/pyversions/multirunnable.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/multirunnable)

Installation by pip:

    >>> pip install multirunnable

It also could install the latest version of _multirunnable_ in GitHub by *git* and *python*:

    >>> git clone https://github.com/Chisanan232/multirunnable.git ./apache-multirunnable
    >>> cd ./apache-multirunnable
    >>> python3 setup.py install

It could run in virtual environment like _virtualenv_ or Docker. 
It's better to clear your own develop environment.


* Python Virtual Environment

Please install virtualenv first:

    >>> pip install virtualenv -U

Initial a Python virtual environment with target directory:

    >>> virtualenv -p python3 ./package_test_env

Activate and switch to the environment:

    >>> source ./package_test_env/bin/activate

Finally, we could install the package and do something with it. <br>
Remember, this is a new environment, so it absolutely doesn't have the packages it has outside.
You could leave it by command _deactivate_:

    >>> deactivate


* PyEnv

Manage the Python environment via _pyenv_. 
Please refer to the pyenv [document](https://github.com/pyenv/pyenv) to install and configure it.
It also could manage Python virtual environment via _pyenv_.

Install and verify the Python versions environment it has:

    >>> pyenv install 3.10.0

    ... # Install logs

    >>> pyenv versions
    * system
      3.10.0

Initialize and create a Python virtual environment:

    >>> pyenv virtualenv 3.10.0 multirunnable-py310

Activate to use Python virtual environment:

    >>> pyenv activate multirunnable-py310

Leaving Python virtual environment:

    >>> pyenv deactivate


* Docker

First of all, make sure that Docker has already:

    >>> docker --version

> ⚠️ Remember: It's not necessary about preparing Python environment with Docker.

You also could verify its brief:

    >>> docker info

Everything is ready, let's start to build image:

    >>> docker build -t multirunnable_client:py37 ./ -f ./Dockerfile_py37

Verify it:

    >>> docker images | grep -E "multirunnable_client"

Run it:

    >>> docker run --name multirunnable_executor_client_py37 multirunnable_client:py37

