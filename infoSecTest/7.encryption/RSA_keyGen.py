from Crypto.PublicKey import RSA

#비대칭키예제1 키 만들기
key = RSA.generate(2048) #2048바이트 : 약 2키로바이트
private_key = key.export_key() #비밀키 생성 : 복호화하는 것
file_out = open("private.pem", "wb")
file_out.write(private_key)

public_key = key.publickey().export_key() #공개키 생성 : 암호화하는 것
file_out = open("receiver.pem", "wb")
file_out.write(public_key)

