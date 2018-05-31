import requests

baseUrl = 'http://www.nate.com'

r = requests.get(baseUrl)
print(r.text)
print(r.status_code)
