import urllib.request
import urllib.parse

data = bytes(urllib.parse.urlencode({"word":"hello"}), encoding='utf8')
print(type(data))
print(data)
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())
# response = urllib.request.urlopen("https://www.python.org")
# print(response.status)
# print(response.getheaders())
# print(response.getheader('Server'))
# print(response.read().decode('utf-8'))
