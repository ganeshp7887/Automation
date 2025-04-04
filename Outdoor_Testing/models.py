from _ast import Expr

from Outdoor_Testing.Outdoor_response_builder import Transaction_Processing
from API.configfile import configFile
import time
import dict2xml
from API.Utility import Utility
import json
import re


class OutdoorModel:

    def __init__(self):
        self.result = {}
        self.utility = Utility()
        self.config = configFile()
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = self.config.Outdoor_request_format()
        self.API_SEQUENCE = self.config.OUTDOOR_API_SEQUENCE().split(",")
        self.isXml = self.RequestFormat.upper() == "XML"

    def TransactionProcessing(self, request, isSingle):

        @staticmethod
        def convert(Data, isSingle) :
            if isSingle :
                res = dict2xml.dict2xml(Data) if self.isXml else json.dumps(Data, sort_keys=False, indent=2)
            else :
                res = Data
            return res

        CHILDTRANSREQUEST,PARENTTRANSREQUEST = None, None
        EncryptionMode = "00"
        request = json.loads(request.body.decode("utf-8")) if isSingle else request.POST       # Read JSON body
        TransactionType = request.get('Trans_type').split("_", 1)
        CardDataSource = request.get('cds')
        rowData = request.get('rowData', {})  # Use get to avoid KeyError
        product_count = request.get('product_count', 0)
        Iteration = request.get('Iteration')
        PinBlockMode = request.get('pbm', "")
        Transaction_total = request.get('Trn_amt', "")
        print(Transaction_total)
        if rowData is not None:
            rowData = rowData if isinstance(rowData, dict) else json.loads(rowData)
            TrackData = rowData.get("TrackData", "")
            EMVDetailsData = rowData.get("EmvDetailsData", "")
            ExpectedCardType = rowData.get("CardType")
            Feature = rowData.get("Feature", None)
            pinData = rowData.get("pinData", None)
            PINBlock = KSNBlock = ""
            if Feature and Feature.upper().replace(" ", "") == "ONLINEPIN" :
                PINBlock, KSNBlock = {
                    "01" : (rowData.get("Omnikey_PinBlock"), rowData.get("Omnikey_KSNBlock")),
                    "00" : (rowData.get("Chasekey_PinBlock"), rowData.get("Chasekey_KSNBlock")),
                    "02" : (rowData.get("Fdkey_PinBlock"), rowData.get("Fdkey_KSNBlock"))
                }.get(PinBlockMode, ("", ""))
                PinBlockMode = "01" if PinBlockMode == "01" else ""
            if pinData:
                PinBlockMode = "01" if pinData == "01" else ""
                PINBlock = rowData.get("PINBlock")
                KSNBlock = rowData.get("KSNBlock")
            Parent_TransactionType = TransactionType[0]
            Child_TransactionType = TransactionType[1] if len(TransactionType) > 1 else None

            print(f'Performing # {Iteration} Transaction of {Child_TransactionType + " of" if Child_TransactionType is not None else ""} {Parent_TransactionType}')

            if Parent_TransactionType and Parent_TransactionType != "000" :
                PARENTTRANSREQUEST = lambda : self.transaction_processor.ParentTransactionProcessing(TransactionType=Parent_TransactionType, TrackData=TrackData, EncryptionMode=EncryptionMode, CardDataSource=CardDataSource, EMVDetailsData=EMVDetailsData,
                                                                                                PINBlock=PINBlock, KSNBlock=KSNBlock, PinBlockMode=PinBlockMode, Transaction_total=Transaction_total, product_count=product_count, TransactionSeqNum=Iteration)
            if Child_TransactionType :
                CHILDTRANSREQUEST = lambda : self.transaction_processor.ChildTransactionProcessing(TransactionType=Child_TransactionType, TrackData=TrackData, EncryptionMode=EncryptionMode, CardDataSource=CardDataSource, EMVDetailsData=EMVDetailsData,
                                                                                                   PINBlock=PINBlock, KSNBlock=KSNBlock, PinBlockMode=PinBlockMode, Transaction_total=Transaction_total, product_count=product_count, TransactionSeqNum=Iteration)

            method_mapping = {
                'GCB' : lambda : self.transaction_processor.GCBTransaction(LookUpFlag=str(api_number), TrackData=TrackData, EncryptionMode=EncryptionMode, CardDataSource=CardDataSource, EMVDetailsData=EMVDetailsData, PINBlock=PINBlock, KSNBlock=KSNBlock, PinBlockMode=PinBlockMode),
                'TRANSREQUEST' : [PARENTTRANSREQUEST, CHILDTRANSREQUEST]
            }
            for api in self.API_SEQUENCE :
                api_name, api_number, api_message, = self.utility.extract_api_details(api)
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
                    "ErrorText" : self.transaction_processor.ErrorText,
                    "RequestFormat" : self.RequestFormat,
                    "TrackData" : TrackData,
                    "ExpectedCardType" : ExpectedCardType
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
                    "ChildOfChild" : {
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