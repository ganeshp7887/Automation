import traceback

from API.Utility import Utility
from API.Socket_API import Adsdk_Socket as socket
from API.configfile import configFile as cn
from Outdoor_Testing.Outdoor_request_builder import Outdoor_Request_Builder

class Transaction_Processing:

    def __init__(self):
        config = cn()
        self.Gcb_Transaction_Request = {}
        self.Gcb_Transaction_Response = {}
        self.Parent_Transaction_request = {}
        self.Parent_Transaction_response = {}
        self.Child_Transaction_response = {}
        self.Child_Transaction_request = {}
        self.Child_of_child_Transaction_request = {}
        self.Child_of_child_Transaction_response = {}


        self.Gcb_Transaction_ResponseCode = None
        self.Gcb_Transaction_ResponseText = None
        self.Gcb_Transaction_CardType = None
        self.Parent_Transaction_ResponseCode = None
        self.Parent_Transaction_TransactionIdentifier = None
        self.Parent_Transaction_ResponseText = None
        self.Parent_Transaction_TransactionAmount = None
        self.Parent_Transaction_AurusPayTicketNum = None
        self.Parent_Transaction_TransactionSequenceNumber = None
        self.Child_Transaction_TransactionIdentifier = None
        self.Child_Transaction_AurusPayTicketNumber = None
        self.Child_Transaction_ResponseText = None
        self.Child_Transaction_ResponseCode = None

        self.Child_of_child_Transaction_ResponseText = None
        self.Child_of_child_TransactionIdentifier = None
        self.Child_of_child_AurusPayTicketNumber = None

        self.ParentTransactionTypeName = None
        self.ChildTransactionTypeName = None
        self.ChildOfChildTransactionTypeName = None

        self.Outdoor_Request_Builder = Outdoor_Request_Builder()
        self.port = config.Config_Outdoor_port()
        self.operations = Utility()
        self.requestFormat = config.Outdoor_request_format()
        self.ip = config.system_ip()
        self.urlExtention = ""
        self.APIurl = ""
        self.isHttps = config.commProtocol() != "5"
        self.url = rf"https://{self.ip}:{self.port}{self.urlExtention}{self.APIurl}"
        self.sock = socket()
        self.ErrorText = ""
        self.requestFrom = "OUTDOOR"


    def GCBTransaction(self, **kwargs):
        try:
            Gcb_Transaction_Req = self.Outdoor_Request_Builder.gcb(**kwargs)
            GCB_Transaction_res = self.sock.handleSocketRequest(Gcb_Transaction_Req,self.requestFrom)
            if GCB_Transaction_res:
                try:
                    self.Gcb_Transaction_Request = self.operations.ConvertToJson(Gcb_Transaction_Req, self.requestFrom)
                    self.Gcb_Transaction_Response = self.operations.ConvertToJson(GCB_Transaction_res, self.requestFrom)
                    self.Gcb_Transaction_ResponseCode = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("ResponseCode", "")
                    self.Gcb_Transaction_ResponseText = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("ResponseText", "")
                    self.Gcb_Transaction_CardType = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("CardType", "")
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.requestFrom else 'JSON' }"
        except Exception as e:
            self.ErrorText = f"Error GCB Transaction :: ==> {e}"

    def ParentTransactionProcessing(self, **kwargs):
        TransType = kwargs.get("TransactionType")
        try:
            kwargs.update(CardType=self.Gcb_Transaction_CardType)
            if kwargs.get("TransactionType") == "02" or (self.Gcb_Transaction_ResponseCode is not None and self.Gcb_Transaction_ResponseCode.startswith("0")):
                Parent_Transaction_req = self.Outdoor_Request_Builder.Parent_Transaction(**kwargs)
                Parent_Transaction_res = self.sock.handleSocketRequest(Parent_Transaction_req,self.requestFrom)
                if Parent_Transaction_res:
                    try:
                        self.Parent_Transaction_request = self.operations.ConvertToJson(Parent_Transaction_req, self.requestFrom)
                        self.Parent_Transaction_response = self.operations.ConvertToJson(Parent_Transaction_res, self.requestFrom)
                        trans_detail = self.Parent_Transaction_response.get("TransResponse", {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0: trans_detail = trans_detail[0]
                        self.Parent_Transaction_ResponseCode = trans_detail.get("ResponseCode", "")
                        self.Parent_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier', "")
                        self.Parent_Transaction_ResponseText = trans_detail.get('ResponseText', "")
                        self.Parent_Transaction_TransactionSequenceNumber = trans_detail.get('TransactionSequenceNumber', "")
                        self.Parent_Transaction_TransactionAmount = trans_detail.get('TotalApprovedAmount', " ")
                        self.Parent_Transaction_AurusPayTicketNum = self.Parent_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum", "")
                        self.ParentTransactionTypeName = "Sale" if TransType == "01" else "Pre-auth" if TransType == "04" else "Refund w/o Sale" if TransType == "02" else "Gift Transactions"
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.requestFrom else 'JSON' }"
        except Exception as e:
            tb = traceback.format_exc()
            self.ErrorText = f"Error in TransactionProcessing: {e}\nTraceback:\n{tb}"

    def ChildTransactionProcessing(self, **kwargs):
        try:
            if self.Parent_Transaction_ResponseCode is not None and self.Parent_Transaction_ResponseCode.startswith("0", 0, 1):
                Transactions = kwargs.get("TransactionType").split("_")
                childTransactionType = Transactions[0]

                Transaction_total = self.Parent_Transaction_TransactionAmount if "06" in childTransactionType.upper() else kwargs.get("Transaction_total")
                kwargs.update(CardType=self.Gcb_Transaction_CardType, TransactionType=childTransactionType, Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier, Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum, TransAmount=Transaction_total)
                if "09" in childTransactionType.upper():
                    kwargs.update(TransactionSeqNum=self.Parent_Transaction_TransactionSequenceNumber)
                    Child_Transaction_req = self.Outdoor_Request_Builder.Parent_Transaction(**kwargs)
                else:
                    Child_Transaction_req = self.Outdoor_Request_Builder.Child_Transaction(**kwargs)
                Child_Transaction_res = self.sock.handleSocketRequest(Child_Transaction_req,self.requestFrom)
                if Child_Transaction_res :
                    self.Child_Transaction_request = self.operations.ConvertToJson(Child_Transaction_req, self.requestFrom)
                    self.Child_Transaction_response = self.operations.ConvertToJson(Child_Transaction_res, self.requestFrom)
                    trans_detail = self.Child_Transaction_response.get("TransResponse", {}).get("TransDetailsData", {}).get("TransDetailData", {})
                    if isinstance(trans_detail, list) and len(trans_detail) > 0: trans_detail = trans_detail[0]
                    self.Child_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier', "")
                    self.Child_Transaction_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                    self.Child_Transaction_ResponseText = trans_detail.get('ResponseText', "")
                    self.Child_Transaction_ResponseCode = trans_detail.get('ResponseCode', "")
                    self.ChildTransactionTypeName = "Refund" if childTransactionType == "02" else "Void" if childTransactionType == "06" else "Post-auth" if childTransactionType == "05" else "CancelLast" if childTransactionType == "76" else None
                    childOfChildTransactionType = Transactions[1] if len(Transactions) > 1 else None
                    if childOfChildTransactionType and self.Child_Transaction_ResponseCode.startswith("0"):
                        kwargs.update(TransactionType=childOfChildTransactionType, Parent_TransactionID=self.Child_Transaction_TransactionIdentifier, Parent_AurusPayTicketNum=self.Child_Transaction_AurusPayTicketNumber)
                        if childOfChildTransactionType == "05":  #post-auth retry scenario
                            kwargs.update(DuplicateTransCheck="1", Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier, Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum)
                        Child_of_child_Transaction = self.Outdoor_Request_Builder.Child_Transaction(**kwargs)
                        Child_of_child_res = self.sock.handleSocketRequest(Child_of_child_Transaction,self.requestFrom)
                        if Child_of_child_res :
                            self.Child_of_child_Transaction_request = Utility.ConvertToJson(Child_of_child_Transaction, self.requestFrom)
                            self.Child_of_child_Transaction_response = Utility.ConvertToJson(Child_of_child_res, self.requestFrom)
                            RequestTopnode = next(iter(self.Child_of_child_Transaction_request))
                            ResponseTopNode = next(iter(self.Child_of_child_Transaction_response))
                            TransType = self.Child_of_child_Transaction_request.get(RequestTopnode, {}).get("TransactionType")
                            trans_detail = self.Child_of_child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                            if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                            self.Child_of_child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                            self.Child_of_child_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                            self.Child_of_child_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                            self.ChildOfChildTransactionTypeName = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
        except Exception as e:
            tb = traceback.format_exc()
            self.ErrorText = f"Error in TransactionProcessing: {e}\nTraceback:\n{tb}"