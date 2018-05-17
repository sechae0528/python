import requests
URL = 'http://192.168.110.116:8090/api/v1/getrecord'
#response = requests.get(URL)
#print(response.status_code)
#print(response.text)

# GET 방식 호출
params = {'key1': 'value1'}
res = requests.get(URL, params=params)

