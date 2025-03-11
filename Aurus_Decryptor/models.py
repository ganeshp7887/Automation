import base64
from Crypto.Cipher import AES

def decrypt(key, data) :
    key =  key.encode('utf-8')
    encrypted_bytes = bytes.fromhex(data)
    cipher = AES.new(key, AES.MODE_ECB)
    cc = cipher.decrypt(encrypted_bytes)
    return cc