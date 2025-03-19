import json
import xmltodict
from lxml import etree
from .configfile import configFile

class Utility :

    @staticmethod
    def readTransactionTypes():
        with open("./TransactionTypes.json", 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def readGiftBins():
        with open("./GiftBin.json", 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def ConvertToXml(data):
        request = xmltodict.unparse(data, encoding=str)
        request = request.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
        return request

    @staticmethod
    def ConvertToJson(data, requestCameFrom):
        request = None
        isXml = configFile().request_format().upper() == "XML" if requestCameFrom.upper() == "INSTORE" else configFile().Outdoor_request_format().upper() == "XML"
        if isXml:
            data =  data.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
            request = xmltodict.parse(etree.tostring(etree.fromstring(data), encoding=str))
        else:
            request = json.loads(data)
        return request

    @staticmethod
    def findNode(request):
        return next(iter(request))