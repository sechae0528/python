import requests

baseUrl = 'http://localhost:'

port = 8052
subUrl = '/api/v1/getrecord'

for i in range (8052, 8078):
    myUrl = baseUrl + str(i) + subUrl
    try:
        r = requests.get(myUrl)
        #print(r)
        #print(r.status_code)
        if r.status_code == 200:
            #print(r.text)
            print("%s 님 성공"% str(i))
            print(r.text)
            print("------------------------------------------")
        else:
            print("%s 님 실패"% str(i))
    except:
         print("%s 님 서비스 안함"% str(i))
         pass

