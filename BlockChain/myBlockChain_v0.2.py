import hashlib
import time
import csv
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
import re
from urllib.parse import parse_qs
from urllib.parse import urlparse
import threading
import cgi

PORT_NUMBER = 8099


class Block:

    # A basic block contains, index (blockheight), the previous hash, a timestamp, tx information, a nonce, and the current hash

    def __init__(self, index, previousHash, timestamp, data, currentHash, proof ):
        self.index = index #블록의 높이
        self.previousHash = previousHash #이전블록의 해쉬값(이전블록의 연결고리, 스냅샷)
        self.timestamp = timestamp #블록생성시점
        self.data = data #거래 데이터
        self.currentHash = currentHash #현재 블록의 해쉬값
        self.proof = proof #작업증명 값(XX횟수)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def generateGenesisBlock():
    print("generateGenesisBlock is called")
    timestamp = time.time()
    print("time.time() => %f \n" % timestamp)
    tempHash = calculateHash(0, '0', timestamp, "My very first block :)", 0)
    print(tempHash)
    return Block(0, '0', timestamp, "My very first block",  tempHash,0)
    # return Block(0, '0', '1496518102.896031', "My very first block :)", 0, '02d779570304667b4c28ba1dbfd4428844a7cab89023205c66858a40937557f8')

def calculateHash(index, previousHash, timestamp, data, proof):
    value = str(index) + str(previousHash) + str(timestamp) + str(data) + str(proof)
    sha = hashlib.sha256(value.encode('utf-8')) #sha256 형식으로 지정된 해시 객체 생성
    return str(sha.hexdigest()) #hexdigest 방법을 이용해 객체로부터 sha256 해시에 대한 16진수 값을 구함

def calculateHashForBlock(block):
    return calculateHash(block.index, block.previousHash, block.timestamp, block.data, block.proof)

def getLatestBlock(blockchain):
    return blockchain[len(blockchain) - 1]

def generateNextBlock(blockchain, blockData, timestamp, proof):
    previousBlock = getLatestBlock(blockchain)
    nextIndex = int(previousBlock.index) + 1
    nextTimestamp = timestamp
    nextHash = calculateHash(nextIndex, previousBlock.currentHash, nextTimestamp, blockData, proof)
    # index, previousHash, timestamp, data, currentHash, proof
    return Block(nextIndex, previousBlock.currentHash, nextTimestamp, blockData, nextHash,proof)

def writeBlockchain(blockchain):
    blockchainList = []

    for block in blockchain:
        # index, previousHash, timestamp, data, currentHash, proof
        blockList = [block.index, block.previousHash, str(block.timestamp), block.data, block.currentHash,block.proof ] #bug fix 20180511 by hwy
        blockchainList.append(blockList)

    with open("blockchain.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(blockchainList)

    print('Blockchain written to blockchain.csv.')

def readBlockchain(blockchainFilePath, mode = 'internal'): #외부에서 들어오는 것은 external 내부에서 조회하는 것은 internal
                                                        # mode 값을 안주면 자동으로 internal 값으로 인식한다.
    print("readBlockchain")
    importedBlockchain = [] # list형식

    try:
        with open(blockchainFilePath, 'r',  newline='') as file: #csv파일을 read모드로 읽겠다. newline : window에서만 사용할 때 필요, 다른 서버에 올릴 때는 필요없음
            blockReader = csv.reader(file) #csv : 여섯개의 정보
            for line in blockReader:
                block = Block(line[0], line[1], line[2], line[3], line[4], line[5])
                importedBlockchain.append(block) #list형식으로 블록이 생김 [Block1], {Block2], [Block3]

        print("Pulling blockchain from csv...")

        return importedBlockchain

    except:
        if mode == 'internal' :
            return [generateGenesisBlock()]
        else :
            return None

def getTxData():
    txData = ''

    for _ in range(5):
        txTo, txFrom, amount = random.randrange(0, 1000), random.randrange(0, 1000), random.randrange(0, 100)
        transaction = 'UserID ' + str(txFrom) + " sent " + str(amount) + ' bitTokens to UserID ' + str(txTo) + ". "
        txData += transaction

    return txData

def mineNewBlock(difficulty=2, blockchainPath='blockchain.csv'):
    blockchain = readBlockchain(blockchainPath)
    txData = getTxData()
    timestamp = time.time()
    proof = 0
    newBlockFound = False

    print('Mining a block...')

    while not newBlockFound:
        newBlockAttempt = generateNextBlock(blockchain, txData, timestamp, proof)
        if newBlockAttempt.currentHash[0:difficulty] == '0' * difficulty: #앞부분에 0이 2개면 빠져나가서 writeBlockChain 해라.
            stopTime = time.time()
            timer = stopTime - timestamp
            print('New block found with proof', proof, 'in', round(timer, 2), 'seconds.')
            newBlockFound = True
        else:
            proof += 1

    blockchain.append(newBlockAttempt)
    writeBlockchain(blockchain)

def mine(blocksToMine=5):
    for _ in range(blocksToMine):
        mineNewBlock()

def isSameBlock(block1, block2): #block1은 db안에, block2는 post로 받은거
    if block1.index != block2.index:
        return False
    elif block1.previousHash != block2.previousHash:
        return False
    elif block1.timestamp != block2.timestamp:
        return False
    elif block1.data != block2.data:
        return False
    elif block1.currentHash != block2.currentHash:
        return False
    elif block1.proof != block2.proof:
        return False
    return True


def isValidNewBlock(newBlock, previousBlock): #새로생성된 블록이 이전블록값과 연결되어있는지 확인
    if int(previousBlock.index) + 1 != int(newBlock.index):
        print('Indices Do Not Match Up')
        return False
    elif previousBlock.currentHash != newBlock.previousHash:
        print("Previous hash does not match")
        return False
    elif calculateHashForBlock(newBlock) != newBlock.currentHash:
        print("Hash is invalid")
        return False
    return True


def isValidChain(bcToValidate):
    genesisBlock = []
    bcToValidateForBlock = []

    # Read GenesisBlock
    try:
        with open('blockchain.csv', 'r') as file:
            blockReader = csv.reader(file)
            for line in blockReader:
                block = Block(line[0], line[1], line[2], line[3], line[4], line[5])
                genesisBlock.append(block)
                break
    except:
        print("file open error in isValidChain")
        pass

    # transform given data to Block object
    for line in bcToValidate:
        # print(type(line))
        # index, previousHash, timestamp, data, currentHash, proof
        block = Block(line['index'], line['previousHash'], line['timestamp'], line['data'], line['currentHash'], line['proof'])
        bcToValidateForBlock.append(block)

    #if it fails to read block data  from db(csv)
    if not genesisBlock:
        print("fail to read genesisBlock")
        return False

    # compare the given data with genesisBlock
    if not isSameBlock(bcToValidateForBlock[0], genesisBlock[0]): #post로 받은 블록과 db안에 있는 블록 비교 같은지
        print('Genesis Block Incorrect')
        return False

    tempBlocks = [bcToValidateForBlock[0]] #post로 받은 블록과 db안에 있는 블록이 같으면 for문을 돌아 블록이 잘 연결되어있는지 확인
    for i in range(1, len(bcToValidateForBlock)):
        if isValidNewBlock(bcToValidateForBlock[i], tempBlocks[i - 1]):
            tempBlocks.append(bcToValidateForBlock[i])
        else:
            return False

    return True


# This class will handle any incoming request from
# a browser
class myHandler(BaseHTTPRequestHandler):


    # Handler for the GET requests
    def do_GET(self):
        data = []  # response json data
        if None != re.search('/block/*', self.path):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            if None != re.search('/block/getBlockData', self.path):
                # TODO: range return (~/block/getBlockData?from=1&to=300) #from ~ to :범위를 정해서 받는게 좋음. 리턴값이 크면 처리하기 힘들기 때문에
                # queryString = urlparse(self.path).query.split('&')

                block = readBlockchain('blockchain.csv', mode = 'external')

                if block == None :
                    print("No Block Exists")
                    data.append("no data exists")
                else :
                    for i in block:
                        print(i.__dict__) #i : 하나하나가 class Block을 뜻함 #__dict__ : 변수명과 변수값을 dictionary형태로 찍어라.
                        data.append(i.__dict__)
                        #data.append(i.toJSON()) # --> 이 방법은 안됨 리턴문자열에 '\' 문자 포함됨

                self.wfile.write(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))

            elif None != re.search('/block/generateBlock', self.path):
                #mine() # thread 로 아래 코드와 같이 분리해야함
                t = threading.Thread(target=mine)
                t.start()
                data.append("{mining is underway:check later by calling /block/getBlockData}")
                self.wfile.write(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
            else:
                data.append("{info:no such api}")
                self.wfile.write(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        # ref : https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/

    def do_POST(self):

        if None != re.search('/block/*', self.path):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            if None != re.search('/block/validateBlock/*', self.path):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                print(ctype)
                print(pdict)

                if ctype == 'application/json':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    receivedData = post_data.decode('utf-8')
                    print(type(receivedData))
                    tempDict = json.loads(receivedData)  # load your str into a list #print(type(tempDict))
                    if isValidChain(tempDict) == True :
                        tempDict.append("validationResult:normal")
                        self.wfile.write(bytes(json.dumps(tempDict), "utf-8"))
                    else :
                        tempDict.append("validationResult:abnormal")
                        self.wfile.write(bytes(json.dumps(tempDict), "utf-8"))

                elif ctype == 'application/x-www-form-urlencoded':
                    content_length = int(self.headers['content-length'])
                    # trouble shooting, below code ref : https://github.com/aws/chalice/issues/355
                    postvars = parse_qs((self.rfile.read(content_length)).decode('utf-8'), keep_blank_values=True)
                    # print(postvars)    #print(type(postvars)) #print(postvars.keys())

                    self.wfile.write(bytes(json.dumps(postvars), "utf-8"))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

try:

    # Create a web server and define the handler to manage the
    # incoming request
    # server = HTTPServer(('', PORT_NUMBER), myHandler)
    #server = ThreadedHTTPServer(('localhost', PORT_NUMBER), myHandler) #localhost에서만 서비스를 돌릴 수 있다.
    server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
