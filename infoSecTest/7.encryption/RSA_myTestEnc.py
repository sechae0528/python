from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

#비대칭키예제 공개키로 암호화
data = "I met aliens in UFO. Here is the map!!!!.".encode("utf-8")
file_out = open("encrypted_data.bin", "wb")

# 공개키 읽어온다
recipient_key = RSA.import_key(open("receiver.pem").read())

# 메세지를 공개키로 암호화
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_msg = cipher_rsa.encrypt(data)

file_out.write(enc_msg)

