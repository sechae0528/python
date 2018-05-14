#!/usr/bin/python
# from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import json
import sys
import re
import os
import urllib.request





PORT_NUMBER = 8073

# This class will handle any incoming request from
# a browser
class myHandler(BaseHTTPRequestHandler):



    # Handler for the GET requests
    def do_GET(self):

        data = {}

        print('Get request received')
        if None != re.search('/api/v1/getrecord/', self.path):


            #recordID = (self.path.split('/')[-1]).split('?')[0]
            #print("recordID = ", recordID)
            #if recordID == "1" :
               # self.send_response(200)
               # self.send_header('Content-type', 'text/html')
               # self.end_headers()
                # Send the html message
                #self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
                #self.wfile.write(bytes("<body><p>Hello python!!</p>", "utf-8"))
                #self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
                #self.wfile.write(bytes("</body></html>", "utf-8"))


                # self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
                # self.wfile.write(bytes("<body>response_body", "utf-8"))
                # self.wfile.write(bytes("<p>response_body</p>" % self.path, "utf-8"))
                # self.wfile.write(bytes("</body></html>", "utf-8"))

                #self.wfile.write(bytes('response_body', "utf-8"))


                #print(json.dumps(data, sort_keys=True, indent=4))
                #self.wfile.write(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))

                client_id = "CJki3_MfJgnCJbjcokve"
                client_secret = "oLiHv9Ur3v"
                encText = urllib.parse.quote("아시아")
                url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # json 결과
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)

                rescode = response.getcode()
                if (rescode == 200):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    response_body = response.read()

                    #print(type(response_body)) : bytes
                    #print(type(response_body.decode('utf-8'))) : str
                    #print(type(response_body.decode('utf-8').encode('EUC-KR'))) : bytes
                    #print(response_body.decode('utf-8'))

                    #self.wfile.write(bytes(json.dumps(aTemp, sort_keys=True, indent=4), "utf-8"))
                    #self.wfile.write(response_body.decode('utf-8').encode('EUC-KR'))
                    self.wfile.write(response_body.decode('utf-8').encode('utf-16'))
                    #response_body = response.read()
                    print(response_body.decode('utf-8'))
                    # jsonString = json.dumps(response_body.decode('utf-8'),indent=4)
                    # print(jsonString)
                    dict = json.loads(response_body.decode('utf-8'))
                    print(dict['items'])
                    for a in dict['items']:
                        print("\n")
                        print("title :" + a['title'])
                        print("\n")
                        print("bloggername :" + a['bloggername'])
                        print("\n")
                        print("link : " + a['bloggerlink'])
                        print("\n")


                else:
                    print("Error Code:" + rescode)



            #else:
               # self.send_response(400, 'Bad Request: record does not exist')
               # self.send_header('Content-Type', 'application/json')
               # self.end_headers()
        else:
           self.send_response(403)
           self.send_header('Content-Type', 'application/json')
           self.end_headers()
        #ref : https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/


        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

try:

    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    #server = ThreadedHTTPServer(('localhost', PORT_NUMBER), myHandler) 자체테스트할 때만 사용('localhost')
    print ('Started httpserver on port ' , PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()