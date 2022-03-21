# import urllib.request
# import json
#
#
# __GitHub_API = 'https://api.github.com/repos/Chisanan232/multirunnable/releases/latest'
#
#
# def __github_tag_version__():
#     __response = urllib.request.urlopen(__GitHub_API)
#     __data = __response.readlines()
#     return json.loads(__data[0].decode('ascii'))["tag_name"]

__github_tag_version__ = "0.17.0a1"

