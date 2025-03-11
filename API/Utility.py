import json

import xmltodict
from lxml import etree

from API.config import config


class Utility :


    @staticmethod
    def readTransactionTypes():
        with open("./TransactionTypes.json", 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def readIndoorFile(filename):
        file_path = rf"{config.Full_Indoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def readOutdoorFile(filename) :
        file_path = rf"{config.Full_Outdoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def ConvertToXml(data):
        request = xmltodict.unparse(data, encoding=str)
        request = request.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
        return request

    @staticmethod
    def ConvertToJson(data, isXml=True):
        request = None
        if isXml:
            data =  data.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
            request = xmltodict.parse(etree.tostring(etree.fromstring(data), encoding=str))
        else:
            request = json.loads(data)
        return request

    @staticmethod
    def findNode(request):
        return next(iter(request))