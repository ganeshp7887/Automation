import json

from django.shortcuts import render
import re

from .models import decrypt
import base64
# Create your views here.

class Aurus_Decryptor:

    def __init__(self) :
        pass

    def find_key(self, data, target_key, results=None):
        target_key = target_key.lower()
        if results is None:
            results = None

        if isinstance(data, dict):
            for key, value in data.items():
                if key.lower() == target_key:
                    results = value
                self.find_key(value, target_key, results)
        return results

    def Decryptor(self, request):
        decrypted_data = ""
        if request.method == 'POST':
            Payload = request.POST.get("encryptedRequest", "")
            Payload = Payload.replace("'", '"')
            Payload = json.loads(Payload, strict=False)
            encryptionFlag = self.find_key(Payload, "encryptionFlag")
            if not encryptionFlag:
                encryptionFlag = self.find_key(Payload, "EncFlag")
                if not encryptionFlag:
                    context = {"EncryptedData" : Payload, "DecryptedData" : 'Encryption flag not found :: Expected ("encryptionFlag", "EncFlag")'}
                    return render(request, 'Aurus_Decryptor.html', context)
            txnDateTime = self.find_key(Payload, "txnDateTime")
            if not txnDateTime:
                txnDateTime = self.find_key(Payload, "DateTime")
                if not txnDateTime:
                    context = {"EncryptedData" : Payload, "DecryptedData" : 'Datetime not found :: Expected ("DateTime")'}
                    return render(request, 'Aurus_Decryptor.html', context)
            response = self.find_key(Payload, "Payload")
            if not response:
                context = {"EncryptedData" : Payload, "DecryptedData" : 'Payload not found :: Expected ("Payload", "PayloadResponse)'}
                return render(request, 'Aurus_Decryptor.html', context)
            response = response.replace("STX", "").replace("ETX", "").split("[FS]")
            responseData = response[2] if encryptionFlag not in ("00", "07") else response[0]
            DataToDecrypt = responseData
            try :
                if encryptionFlag == "00":
                    decrypted_data = bytes.fromhex(DataToDecrypt)
                    decrypted_data = str(decrypted_data.decode('utf-8'))
                if encryptionFlag == "07":
                    decrypted_data = base64.b64decode(DataToDecrypt)
                    decrypted_data = str(decrypted_data.decode('utf-8'))
                if encryptionFlag in ("05", "02") :
                    static_key = f"K@P!T0!HAP45$IUE5K{txnDateTime}"
                    decryptText = decrypt(static_key, DataToDecrypt)
                    decrypted_data = base64.b64decode(decryptText) if encryptionFlag == "05" else decryptText
                    decrypted_data = str(decrypted_data.decode('utf-8'))
                if encryptionFlag in ("01", "03", "06"):
                    deviceSerialNumber = request.POST.get("deviceSerialNumber", "")
                    static_key = f"5UC355K3Y{deviceSerialNumber}{txnDateTime}"
                    decryptText = decrypt(static_key, DataToDecrypt)
                    decrypted_data = base64.b64decode(decryptText) if encryptionFlag in ("00","06") else decryptText
                    decrypted_data = str(decrypted_data.decode('utf-8'))
            except Exception as e :
                decrypted_data = f"Decryption Failed : {e}"
            context = {"EncryptedData" : Payload, "DecryptedData" : decrypted_data}
            return render(request, 'Aurus_Decryptor.html', context)
        return render(request, 'Aurus_Decryptor.html')