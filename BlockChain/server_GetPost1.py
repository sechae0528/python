#!/usr/bin/python
# from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import json
import re
from urllib.parse import parse_qs
from urllib.parse import urlparse
import cgi # 어플리케이션 타입확인하기 위해 사용
import urllib.request

PORT_NUMBER = 8073

# This class will handle any incoming request from
# a browser
class myHandler(BaseHTTPRequestHandler):


    # Handler for the GET requests
    def do_GET(self):

        print('Get request received')
        if None != re.search('/api/v1/getrecord/*', self.path): # url이 http://~/api/v1/getrecord/~ 형태인지 검사

            queryString = urlparse(self.path).query.split('=')[1]  # url이 /api/v1/getrecord?key=value 형태에서 value값을 찾는다.

            print("queryString = ", queryString)
            if None != queryString :
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
                self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
                self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<p>Your query: %s</p>" % queryString, "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))

            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

    def do_POST(self):
        if None != re.search('/api/v1/addrecord', self.path):

            client_id = "CJki3_MfJgnCJbjcokve"
            client_secret = "oLiHv9Ur3v"
            #encText = urllib.parse.quote("아시아")
            #url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # json 결과


            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            print(ctype)
            print(pdict)

            if ctype == 'application/json':

                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                receivedData = post_data.decode('utf-8')
                encText = urllib.parse.quote(receivedData)
                url = "https://openapi.naver.com/v1/search/blog?query=" + encText
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()

                print(type(receivedData))
                tempDict = json.loads(receivedData) #  load your str into a dict
                tempDict.update({'author': 'cse'})
                print(type(tempDict))
                print(tempDict)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(tempDict), "utf-8"))

            elif ctype == 'application/x-www-form-urlencoded':
                content_length = int(self.headers['content-length'])
                # trouble shooting, below code ref : https://github.com/aws/chalice/issues/355
                postvars = parse_qs((self.rfile.read(content_length)).decode('utf-8'),keep_blank_values=True)

                print(postvars)
                print(type(postvars))
                print(postvars.keys())

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(postvars) ,"utf-8"))
            else:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        # ref : https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/


        return


try:

    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
