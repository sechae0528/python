import requests
#URL = 'http://192.168.110.116:8090/api/v1/getrecord'
URL = 'http://www.naver.com'

#response = requests.get(URL)
#print(response.status_code)
#print(response.text)

# GET 방식 호출
params = {'key1': 'smrt0073'}
res = requests.get(URL, params=params)

print(res)