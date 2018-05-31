from html.parser import HTMLParser

import urllib.request

class myParser(HTMLParser):
    def handle_starttag(self, tag, attrs): #<a href "http"...
        if (tag == "a"):
            for (attr, value) in attrs:
                #print("attr " + attr)
                #print("value " + value)
                if (attr == 'href' and value.startswith("http") == True) :
                    print(value)

url = "https://www.naver.com"
request = urllib.request
response = request.urlopen(url)
tempStr = response.read().decode("utf-8")
print(tempStr) #html코드

parser = myParser()
parser.feed(tempStr)
