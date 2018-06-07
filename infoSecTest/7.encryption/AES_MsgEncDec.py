from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time

#대칭키응용예제
#암호화
key = get_random_bytes(16)
print(key)
cipher = AES.new(key, AES.MODE_EAX)
data = b"This is a test." #바뀌는 부분
ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open("encrypted.bin", "wb") #writr binary모드로 쓰겠다.
[file_out.write(x) for x in (cipher.nonce, tag, ciphertext)] #nonce, tag : 16바이트 다 write해서 붙인다.

file_out.close()

time.sleep(1)

#복호화
file_in = open("encrypted.bin", "rb")
nonce, tag, ciphertext = (file_in.read(x) for x in (16, 16, -1))
#16바이트 읽어서 nonce에 넣어주고, 16바이트 읽어서 tag에 넣어주고, 가장 마지막을 읽어 ciphertext에 넣어라

# print(nonce)
# print(tag)
# print(ciphertext)
# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(data)

file_in.close()