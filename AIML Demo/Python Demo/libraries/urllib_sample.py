from urllib.request import urlopen
response = urlopen("http://python.org/")
print(response.headers)