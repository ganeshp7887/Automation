import json
import re
import time

import dict2xml
from django.http import JsonResponse
from django.shortcuts import render

from API.configfile import configFile
from Response_Builder.Instore_response_builder import Transaction_Processing
from API.Utility import Utility


class InstoreTesting:

    def __init__(self):
        self.result  = {
            "Transactions" : Utility.readTransactionTypes(),
        }
        self.api_patterns = {
            "GETSTATUS" : r"(GETSTATUSREQUEST|GETSTATUS|STATUS)(\d*)(?:\(\"(.+?)\"\))?",
            "SHOWSCREEN" : r"(SHOWSCREENREQUEST|SHOWSCREEN|SCREENREQUEST)(\d*)(?:\(\"(.+?)\"\))?",
            "GCB" : r"(GCB|GCBCHECK|GETCARDBINREQUEST|GETCARDBIN)(\d*)(?:\(\"(.+?)\"\))?",
            "CCTTICKETDISPLAYREQUEST" : r"(CCTTICKETDISPLAYREQUEST)(\d*)(?:\(\"(.+?)\"\))?",
            "GETUSERINPUT" : r"(GETUSERINPUTREQUEST|GETUSERINPUT)(\d*)(?:\(\"(.+?)\"\))?",
            "SHOWLIST" : r"(SHOWLISTREQUEST|SHOWLIST)(\d*)(?:\(\"(.+?)\"\))?",
            "BYPASS" : r"(BYPASSREQUEST|BYPASS|BYPASSSCREENREQUEST|BYPASSSCREEN)(\d*)(?:\(\"(.+?)\"\))?",
            "TIMEDELAY" : r"(TIMEDELAY|TIMEWAIT)(\d*)(?:\(\"(.+?)\"\))?",
            "RESTARTCCTREQUEST" : r"(RESTARTCCT|RESTARTCCTREQUEST|CCTRESTART)(\d*)(?:\(\"(.+?)\"\))?",
            "TRANSREQUEST" : r"(TRANSREQUEST|TRANSACTIONREQUEST|TRANSACTION|TRANS)(\d*)(?:\(\"(.+?)\"\))?",
            "CLOSEREQUEST" : r"(CLOSEREQUEST|CLOSETRANSACTIONREQUEST|CLOSE|CLOSETRANS)(\d*)(?:\(\"(.+?)\"\))?"
        }
        self.RequestFormat = "JSON"
        self.API_SEQUENCE = []
        self.isXml = False

    def format_data(self, data, singleTransactionCheck):
        if singleTransactionCheck == "1":
             return dict2xml.dict2xml(data) if self.isXml else json.dumps(data, sort_keys=False, indent=2)
        else:
            return data

    def extract_api_details(self, api_string):
        bypassEnabled, statusEnabled = False, False
        for api_name, pattern in self.api_patterns.items():
            api_string = api_string.upper().strip()
            if "BYPASS" in api_string:
                bypassEnabled = True
                api_string = api_string.replace("BYPASS", "")
            if "GETSTATUS" in api_string or "GETSTATUSREQUEST" in api_string:
                statusEnabled = True
                api_string = api_string.replace("GETSTATUS", "").replace("GETSTATUSREQUEST", "")
            match = re.match(pattern, api_string, re.IGNORECASE)
            if match:
                number = match.group(2) if match.group(2) else str("4") if "BIN" in api_string else "0"
                message = match.group(3) if match.group(3) else "Enter Message in API"  # Extract message (optional)
                return api_name, number, message, bypassEnabled, statusEnabled
        return api_string, None, "", bypassEnabled, statusEnabled  # Return original name if no match

    def Instore_Testing(self, request):
        if request.method == 'POST':
            config = configFile()
            transaction_processor = Transaction_Processing()
            self.RequestFormat = config.request_format().upper()
            self.API_SEQUENCE = config.API_SEQUENCE().split(",")
            self.isXml = self.RequestFormat == "XML"
            parentTransactionType, childTransactionType, CHILDTRANSREQUEST, PARENTTRANSREQUEST = None, None,None, None
            Transaction_type = request.POST.get('Trans_type', None).split("_", 1)
            singleTransactionCheck = request.POST.get('singleTransactionCheck', '0')
            Iteration = request.POST.get('Iteration', "1")
            AllowKeyedEntry = request.POST.get('gcb_type', "N")
            Token_type = request.POST.get('token_type', "01")
            product_count = int(request.POST.get('product_count', 0))
            amount = None if not request.POST.get('amount') else request.POST.get('amount', None)
            parentTransactionType = Transaction_type[0]
            childTransactionType = Transaction_type[1] if len(Transaction_type) > 1 else None
            if parentTransactionType and parentTransactionType != "000":
                PARENTTRANSREQUEST = lambda : transaction_processor.ParentTransactionProcessing(AllowKeyedEntry=AllowKeyedEntry, ProductCount=product_count, TransactionToken=Token_type, TransactionType=parentTransactionType, childTransactionType=childTransactionType, TransactionAmount=amount)
            if childTransactionType:
                CHILDTRANSREQUEST = lambda : transaction_processor.ChildTransactionProcessing(ProductCount=product_count ,TransactionType=childTransactionType, TransactionAmount=amount)

            print(f'Performing # {Iteration} Transaction of {childTransactionType + " of" if childTransactionType is not None else ""} {parentTransactionType}')

            method_mapping = {
                'GETSTATUS': lambda : transaction_processor.GetStatusRequest(bypassEnabled, getStatusEnabled),
                'TIMEDELAY': lambda : time.sleep(float(api_message)),
                'SHOWLIST': lambda : transaction_processor.SHOWLIST(str(api_number), bypassEnabled, getStatusEnabled),
                'CCTTICKETDISPLAYREQUEST': lambda: transaction_processor.displayTicket(int(api_number), bypassEnabled, getStatusEnabled),
                'GCB': lambda: transaction_processor.GCBTransaction(TransactionType=parentTransactionType, AllowKeyedEntry=AllowKeyedEntry, LookUpFlag=str(api_number), TransactionToken=Token_type, TransactionAmount=amount, bypassEnabled=bypassEnabled, getstatusEnabled=getStatusEnabled),
                'GETUSERINPUT': lambda: transaction_processor.GETUSERINPUT(str(api_message), str(api_number), bypassEnabled, getStatusEnabled),
                'SHOWSCREEN': lambda : transaction_processor.SHOWSCREEN(str(api_message), str(api_number),  bypassEnabled, getStatusEnabled),
                'TRANSREQUEST': [PARENTTRANSREQUEST, CHILDTRANSREQUEST],
                'RESTARTCCTREQUEST' : lambda : transaction_processor.RestartCCTRequestTransaction(),
                'CLOSEREQUEST' : lambda :transaction_processor.CLOSETransaction()
            }

            # Process each API in sequence
            for api in self.API_SEQUENCE :
                api_name, api_number, api_message, bypassEnabled, getStatusEnabled = self.extract_api_details(api)
                method_name = api_name.upper().strip()
                method = method_mapping.get(method_name)
                if isinstance(method, list):
                    for sub_method in method:
                        if sub_method is not None:
                            sub_method()  # Assuming each item in the list is callable
                elif callable(method):
                    method()  # Call the function
                else:
                    print(f"Method {method_name} not found or is not callable.")
                context = {
                    "Data": {
                        "CountApiPerfomed" : "3" if transaction_processor.ChildOfChildTransactionTypeName else "4" if transaction_processor.ChildTransactionTypeName else "6" if transaction_processor.ParentTransactionTypeName else "12",
                        "GCBResponseText" : transaction_processor.Gcb_Transaction_ResponseText,
                        "GCBCardType" : transaction_processor.Gcb_Transaction_CardType,
                        "ParentTransactionID" : transaction_processor.Parent_Transaction_TransactionIdentifier,
                        "ParentResponseText" : transaction_processor.Parent_Transaction_ResponseText,
                        "ChildTransactionID" : transaction_processor.Child_Transaction_TransactionIdentifier,
                        "ChildResponseText" : transaction_processor.Child_Transaction_ResponseText,
                        "ChildofchildTransactionID" : transaction_processor.Child_of_child_TransactionIdentifier,
                        "ChildofchildResponseText" : transaction_processor.Child_of_child_Transaction_ResponseText,
                        "gcb" : "GCB Transaction",
                        "Parent_TransactionType" : f"{transaction_processor.ParentTransactionTypeName} Transaction" if transaction_processor.ParentTransactionTypeName else None,
                        "Child_TransactionType" : f"{transaction_processor.ChildTransactionTypeName} Transaction" if transaction_processor.ChildTransactionTypeName else None,
                        "ChildofChildTransactionType" :f"{transaction_processor.ChildOfChildTransactionTypeName} Transaction" if transaction_processor.ChildOfChildTransactionTypeName else None,
                        "ErrorText" : transaction_processor.ErrorText,
                        "RequestFormat" : self.RequestFormat,
                    },
                    "Result": {
                        key: self.format_data(getattr(transaction_processor, attr), singleTransactionCheck)
                        for key, attr in {
                            "GCB_request": "Gcb_Transaction_Request",
                            "GCB_response": "Gcb_Transaction_Response",
                            "Parent_Transaction_request": "Parent_Transaction_request",
                            "Parent_Transaction_response": "Parent_Transaction_response",
                            "Child_Transaction_request": "Child_Transaction_request",
                            "Child_Transaction_response": "Child_Transaction_response",
                            "Child_of_child_Transaction_request": "Child_of_child_Transaction_request",
                            "Child_of_child_Transaction_response": "Child_of_child_Transaction_response"
                        }.items()
                    },
                }
            self.result.update(context)
            return (render(request, 'Single_Instore_Testing.html', self.result) if singleTransactionCheck == "1" else JsonResponse(self.result, safe=False))
        else:
            return render(request, 'Instore_Testing.html',  self.result)