from Instore_Testing.Instore_response_builder import Transaction_Processing
from API.configfile import configFile
import time
import dict2xml
from API.Utility import Utility
import json

class InstoreModel:

    def __init__(self):
        self.Utility = Utility()
        self.config = configFile()
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = self.config.request_format().upper()
        self.API_SEQUENCE = self.config.API_SEQUENCE().split(",")
        self.isXml = self.RequestFormat == "XML"
        self.result = {}

    def bypassModel(self):
        DATA =  self.transaction_processor.BYPASSTransaction("0")
        return DATA

    def TransactionProcessing(self, request, isSingle) :

        @staticmethod
        def convert(Data, isSingle) :
            if isSingle :
                res = dict2xml.dict2xml(Data) if self.isXml else json.dumps(Data, sort_keys=False, indent=2)
            else :
                res = Data
            return res

        parentTransactionType, childTransactionType, CHILDTRANSREQUEST, PARENTTRANSREQUEST = None, None, None, None
        request = json.loads(request.body.decode("utf-8")) if isSingle else request.POST  # Read JSON body
        Transaction_type = request.get('Trans_type', None).split("_", 1)
        Iteration = request.get('Iteration', "1")
        AllowKeyedEntry = request.get('gcb_type', "N")
        Token_type = request.get('token_type', "01")
        product_count = int(request.get('product_count', 0))
        amount = None if not request.get('amount') else request.get('amount', None)
        parentTransactionType = Transaction_type[0]
        childTransactionType = Transaction_type[1] if len(Transaction_type) > 1 else None
        if parentTransactionType and parentTransactionType != "000" :
            PARENTTRANSREQUEST = lambda : self.transaction_processor.ParentTransactionProcessing(AllowKeyedEntry=AllowKeyedEntry, ProductCount=product_count, TransactionToken=Token_type, TransactionType=parentTransactionType, childTransactionType=childTransactionType, TransactionAmount=amount)
        if childTransactionType :
            CHILDTRANSREQUEST = lambda : self.transaction_processor.ChildTransactionProcessing(ProductCount=product_count, TransactionType=childTransactionType, TransactionAmount=amount)

        print(f'Performing # {Iteration} Transaction of {childTransactionType + " of" if childTransactionType is not None else ""} {parentTransactionType}')

        method_mapping = {
            'GETSTATUS' : lambda : self.transaction_processor.GetStatusRequest(),
            'TIMEDELAY' : lambda : time.sleep(float(api_message)),
            'SHOWLIST' : lambda : self.transaction_processor.SHOWLIST(str(api_number)),
            'CCTTICKETDISPLAYREQUEST' : lambda : self.transaction_processor.displayTicket(int(api_number)),
            'GCB' : lambda : self.transaction_processor.GCBTransaction(TransactionType=parentTransactionType, AllowKeyedEntry=AllowKeyedEntry, LookUpFlag=str(api_number), TransactionToken=Token_type, TransactionAmount=amount),
            'GETUSERINPUT' : lambda : self.transaction_processor.GETUSERINPUT(str(api_message), str(api_number)),
            'SHOWSCREEN' : lambda : self.transaction_processor.SHOWSCREEN(str(api_message), str(api_number)),
            'TRANSREQUEST' : [PARENTTRANSREQUEST, CHILDTRANSREQUEST],
            'RESTARTCCTREQUEST' : lambda : self.transaction_processor.RestartCCTRequestTransaction(),
            'CLOSEREQUEST' : lambda : self.transaction_processor.CLOSETransaction()
        }

        # Process each API in sequence
        for api in self.API_SEQUENCE :
            api_name, api_number, api_message, = self.Utility.extract_api_details(api)
            method_name = api_name.upper().strip()
            method = method_mapping.get(method_name)
            if isinstance(method, list) :
                for sub_method in method :
                    if sub_method is not None :
                        sub_method()  # Assuming each item in the list is callable
            elif callable(method) :
                method()  # Call the function
            else :
                print(f"Method {method_name} not found or is not callable.")
            context = {
                "Data" : {
                    "CountApiPerfomed" : "3" if self.transaction_processor.ChildOfChildTransactionTypeName else "4" if self.transaction_processor.ChildTransactionTypeName else "6" if self.transaction_processor.ParentTransactionTypeName else "12",
                    "ErrorText" : self.transaction_processor.ErrorText,
                    "RequestFormat" : self.RequestFormat,
                },
                "Report" : {
                        "GCB" : {
                            "TransactionType" : "GCB",
                            "Request" : convert(self.transaction_processor.Gcb_Transaction_Request, isSingle),
                            "Response" : convert(self.transaction_processor.Gcb_Transaction_Response, isSingle),
                            "ResponseText" : self.transaction_processor.Gcb_Transaction_ResponseText,
                            "TransactionID" : "",
                            "CardType" : self.transaction_processor.Gcb_Transaction_CardType,
                        },
                        "Parent" : {
                            "TransactionType" : f"{self.transaction_processor.ParentTransactionTypeName} Transaction" if self.transaction_processor.ParentTransactionTypeName else None,
                            "Request" : convert(self.transaction_processor.Parent_Transaction_request, isSingle),
                            "Response" : convert(self.transaction_processor.Parent_Transaction_response, isSingle),
                            "ResponseText" : self.transaction_processor.Parent_Transaction_ResponseText,
                            "TransactionID" : self.transaction_processor.Parent_Transaction_TransactionIdentifier,
                        },
                        "Child" : {
                            "TransactionType" : f"{self.transaction_processor.ChildTransactionTypeName} Transaction" if self.transaction_processor.ChildTransactionTypeName else None,
                            "Request" : convert(self.transaction_processor.Child_Transaction_request, isSingle),
                            "Response" : convert(self.transaction_processor.Child_Transaction_response, isSingle),
                            "ResponseText" : self.transaction_processor.Child_Transaction_ResponseText,
                            "TransactionID" : self.transaction_processor.Child_Transaction_TransactionIdentifier,
                        },
                        "ChildOfChild" :{
                            "TransactionType" : f"{self.transaction_processor.ChildOfChildTransactionTypeName} Transaction" if self.transaction_processor.ChildOfChildTransactionTypeName else None,
                            "Request" : convert(self.transaction_processor.Child_of_child_Transaction_request, isSingle),
                            "Response" : convert(self.transaction_processor.Child_of_child_Transaction_response, isSingle),
                            "ResponseText" : self.transaction_processor.Child_of_child_Transaction_ResponseText,
                            "TransactionID" : self.transaction_processor.Child_of_child_TransactionIdentifier,
                        }
                },
            }
            self.result.update(context)
        return self.result