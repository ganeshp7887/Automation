import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def decrypt(key, data) :
    key =  key.encode('utf-8')
    encrypted_bytes = bytes.fromhex(data)
    cipher = AES.new(key, AES.MODE_ECB)
    cc = cipher.decrypt(encrypted_bytes)
    return cc


def decryptData(key, data):
    key =  key.encode('utf-8')
    encrypted_bytes = bytes.fromhex(data)
    decipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(decipher.decrypt(encrypted_bytes), AES.block_size)  # Remove padding
    print(f" this is  {decrypted_data.decode('utf-8')}")
    return decrypted_data