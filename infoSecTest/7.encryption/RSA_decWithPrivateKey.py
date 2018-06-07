from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

#대칭키를 비대칭키로 한번더 암호화하는 예제 (비밀키로 '대칭키'암호화)
file_in = open("encrypted_data.bin", "rb")

# 비대칭키 읽어온다.
private_key = RSA.import_key(open("private.pem").read())

# 공개키로 암호화된 대칭키, 공개키 정보를 읽는다.
enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

# Decrypt the session key with the private RSA key
# 비밀키로 복호화한다.
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(data.decode("utf-8"))

