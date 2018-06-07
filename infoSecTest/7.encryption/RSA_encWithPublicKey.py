from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

#대칭키를 비대칭키로 한번더 암호화하는 예제 (공개키로 '대칭키'암호화)
data = "I met aliens in UFO. Here is the map.".encode("utf-8")
file_out = open("encrypted_data.bin", "wb")

# 공개키 읽어온다
recipient_key = RSA.import_key(open("receiver.pem").read())
# 대칭키 AES 에 사용할 16바이트 랜덤 키값 생성
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
# 대칭키를 비대칭키(Public Key)로 암호화
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ] #대칭키 풀 때 필요한 것들을 집어넣어줌

