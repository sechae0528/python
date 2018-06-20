import requests
URL = 'http://localhost:8090/api/v1/addrecord'


# POST 방식 호출 (application/x-www-form-urlencoded)
data = {'key1': 'value1', 'key2': 'value'}
res = requests.post(URL, data=data)
print(res)





