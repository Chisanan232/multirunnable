import urllib.request
import json


__GitHub_API = 'https://api.github.com/repos/Chisanan232/multirunnable/releases/latest'

__version__ = "0.16.1"


def __github_tag_version__():
    __response = urllib.request.urlopen(__GitHub_API)
    __data = __response.readlines()
    return json.loads(__data[0].decode('ascii'))["tag_name"]
