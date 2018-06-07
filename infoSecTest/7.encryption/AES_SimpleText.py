from Crypto.Cipher import AES

#대칭키예제
#암호화
key = b'Sixteen byte key' #16바이트 키
cipher = AES.new(key, AES.MODE_EAX) #전체 데이터를 암호화함을 cipher라고 지정
print(cipher)
nonce = cipher.nonce #임의의 값 생성, 키가 유효한지 검사해주는 값
print(nonce)
data=b"8073" #바뀌는 부분!! 암호할 데이터 : 222
ciphertext, tag = cipher.encrypt_and_digest(data)  #ciphertext : tag가 유효한지 검사해주는 값
print(ciphertext) #ciphertext : 암호화된 데이터
print(tag) #tag : 암호화된 데이터가 유효하냐

#복호화
# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce) #key를 알아야 풀수 있음
data = cipher.decrypt_and_verify(ciphertext, tag) #ciphertext, tag도 받아야함
print(data)


