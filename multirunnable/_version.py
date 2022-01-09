import urllib.request
import json

__GitHub_API = 'https://api.github.com/repos/Chisanan232/multirunnable/releases/latest'
__response = urllib.request.urlopen(__GitHub_API)
__data = __response.readlines()
_github_tag_version__ = json.loads(__data[0].decode('ascii'))["tag_name"]
__version__ = "0.15.2"
