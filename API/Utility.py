import json
import xmltodict
from lxml import etree
import re

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
        from .configfile import configFile
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


    def APIPatterns(self):
        addtionalData = '(\d*)(?:\(\"(.+?)\"\))?'
        APIpatterns = {
            "GETSTATUS" : fr"(GETSTATUSREQUEST|GETSTATUS|STATUS){addtionalData}",
            "SHOWSCREEN" : fr"(SHOWSCREENREQUEST|SHOWSCREEN|SCREENREQUEST){addtionalData}",
            "GCB" : fr"(GCB|GCBCHECK|GETCARDBINREQUEST|GETCARDBIN){addtionalData}",
            "CCTTICKETDISPLAYREQUEST" : fr"(CCTTICKETDISPLAYREQUEST|DISPLAYTICKET|TICKETDISPLAY|TICKET|PRODUCT|PRODUCTS){addtionalData}",
            "GETUSERINPUT" : fr"(GETUSERINPUTREQUEST|GETUSERINPUT|USERINPUT){addtionalData}",
            "SHOWLIST" : fr"(SHOWLISTREQUEST|SHOWLIST){addtionalData}",
            "BYPASS" : fr"(BYPASSREQUEST|BYPASS|BYPASSSCREENREQUEST|BYPASSSCREEN){addtionalData}",
            "TIMEDELAY" : fr"(TIMEDELAY|TIMEWAIT){addtionalData}",
            "RESTARTCCTREQUEST" : fr"(RESTARTCCT|RESTARTCCTREQUEST|CCTRESTART){addtionalData}",
            "TRANSREQUEST" : fr"(TRANSREQUEST|TRANSACTIONREQUEST|TRANSACTION|TRANS){addtionalData}",
            "CLOSEREQUEST" : fr"(CLOSEREQUEST|CLOSETRANSACTIONREQUEST|CLOSE|CLOSETRANS){addtionalData}"
        }
        return APIpatterns

    def extract_api_details(self, api_string) :
        api = self.APIPatterns()
        for api_name, pattern in api.items() :
            api_string = api_string.upper().strip()
            match = re.match(pattern, api_string, re.IGNORECASE)
            if match :
                number = match.group(2) if match.group(2) else str("4") if "BIN" in api_string else "0"
                message = match.group(3) if match.group(3) else "Enter Message in API"  # Extract message (optional)
                return api_name, number, message
        return api_string, None, ""  # Return original name if no match