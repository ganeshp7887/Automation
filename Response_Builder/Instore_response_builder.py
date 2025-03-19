import json
import random
import traceback
from API.Utility import Utility
from API.Socket_API import Adsdk_Socket as sock
from API.configfile import configFile
from Request_Builder.Instore_request_builder import Transaction_Request_Builder
from  API.Logger import Logger


class Transaction_Processing :

    def __init__(self):
        self.Gcb_Transaction_Request = {}
        self.Gcb_Transaction_Response = {}
        self.Parent_Transaction_request = {}
        self.Parent_Transaction_response = {}
        self.Child_Transaction_response = {}
        self.Child_Transaction_request = {}
        self.Child_of_child_Transaction_request = {}
        self.Child_of_child_Transaction_response = {}

        self.GETUSERINPUT_Request = {}
        self.GETUSERINPUT_Response = {}

        self.Gcb_Transaction_CardType = None
        self.Gcb_Transaction_ResponseCode = None
        self.Gcb_Transaction_ResponseText = None
        self.Gcb_Transaction_CardToken = None
        self.Gcb_Transaction_CIToken = None
        self.Gcb_Transaction_CRMToken = None
        self.Gcb_Transaction_CashbackAmount = None

        self.GetUserInput_inputText = None

        self.Parent_Transaction_ResponseCode = None
        self.Parent_Transaction_ResponseText = None
        self.Parent_Transaction_TransactionAmount = None
        self.Parent_Transaction_TransactionIdentifier = None
        self.Parent_Transaction_AurusPayTicketNum = None

        self.Child_Transaction_ResponseText = None
        self.Child_Transaction_ResponseCode = None
        self.Child_Transaction_TransactionIdentifier = None
        self.Child_Transaction_AurusPayTicketNumber = None

        self.Child_of_child_Transaction_ResponseText = None
        self.Child_of_child_TransactionIdentifier = None
        self.Child_of_child_AurusPayTicketNumber = None

        self.RandomNumberForInvoice = random.randint(100000, 999999)
        self.requestCameFrom = "Instore"
        self.ChildTransactionType = None
        self.ChildOfChildTransactionType = None
        self.ErrorText = None
        self.tokenForTransaction = ""
        self.ParentTransactionTypeName = None
        self.ChildTransactionTypeName = None
        self.ChildOfChildTransactionTypeName = None
        self.log = Logger()
        self.Transaction_Request_Builder = Transaction_Request_Builder()

    def handleSocketRequest(self, request_data, bypassEnabled, getstatusEnabled) :
        socket = sock()
        config = configFile()
        ip = config.system_ip()
        port = config.Config_Indoor_port()
        url = f"https://{ip}:{port}"
        isHttps = config.commProtocol() != "5"
        requestFormat = config.request_format()
        isXml = requestFormat.upper() == "XML"

        if not isXml: request_data = json.loads(request_data)
        if isHttps :
            try:
                socket.openSocket(port=port)
                try:
                    socket.sendRequest(str(request_data))
                    try:
                        if bypassEnabled:
                            socket.sendRequest(str(self.Transaction_Request_Builder.ByPassScreenRequest("0")))
                            socket.receiveResponseFromSocket()
                        if getstatusEnabled:
                            socket.sendRequest(str(self.Transaction_Request_Builder.GetStatusRequest()))
                            socket.receiveResponseFromSocket()
                        response = socket.receiveResponseFromSocket()
                        return response
                    except Exception as e:
                        self.ErrorText = f"Response not received from @ {ip}::{port} ==> {e}"
                except Exception as e:
                    self.ErrorText = f"Request send Fails @ {ip}::{port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Connection Fails @ {ip}::{port} ==> {e}"
        else :
            try:
                socket.httpsRequest(url, request_data, requestFormat.lower())
                try:
                    if bypassEnabled:
                        socket.httpsRequest(url,str(self.Transaction_Request_Builder.ByPassScreenRequest("0")),requestFormat.lower())
                        socket.receiveResponsehttps()
                    if getstatusEnabled:
                        socket.httpsRequest(url,str(self.Transaction_Request_Builder.GetStatusRequest()),requestFormat.lower())
                        socket.receiveResponsehttps()
                    response = socket.receiveResponsehttps()
                    return response
                except Exception as e:
                    self.ErrorText = f"Received response Fails @ {ip}::{port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Connection Fails @ {ip}::{port} ==> {e}"

    def GetStatusRequest(self, bypassEnabled, getstatusEnabled) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.GetStatusRequest(),bypassEnabled, getstatusEnabled)
        except Exception as e: self.ErrorText = f"Error in GetStatusRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def RestartCCTRequestTransaction(self):
        try : self.handleSocketRequest(self.Transaction_Request_Builder.RestartCCTRequest(), False, False)
        except Exception as e: self.ErrorText = f"Error in RestartCCTRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def Signature(self) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.SignatureRequest(),False, False)
        except Exception as e: self.ErrorText = f"Error in Signature: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def displayTicket(self, productCount,bypassEnabled, getstatusEnabled) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.CCTTicketDisplayRequest(productCount),bypassEnabled, getstatusEnabled)
        except Exception as e: self.ErrorText = f"Error in displayTicket: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWLIST(self, OptionsType, bypassEnabled, getstatusEnabled) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ShowListRequest(OptionsType),bypassEnabled, getstatusEnabled)
        except Exception as e :   self.ErrorText = f"Error in SHOWLIST: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def BYPASSTransaction(self, bypassoption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ByPassScreenRequest(bypassoption), False, False)
        except Exception as e :  self.ErrorText = f"Error in Bypass: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWSCREEN(self, message, flag,bypassEnabled, getstatusEnabled) :
        try :
            message2 = self.GetUserInput_inputText if self.GetUserInput_inputText else ""
            self.handleSocketRequest(self.Transaction_Request_Builder.ShowScreenRequest(str(message), str(message2), flag),bypassEnabled, getstatusEnabled)
        except Exception as e : self.ErrorText = f"Error in SHOWSCREEN: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def GETUSERINPUT(self, message, option,bypassEnabled, getstatusEnabled) :
        """Get user input."""
        try :
            gui = self.Transaction_Request_Builder.GetUserInputRequest(message, option)
            guiResponse = self.handleSocketRequest(gui, bypassEnabled, getstatusEnabled)
            if guiResponse:
                self.GETUSERINPUT_Request = Utility.ConvertToJson(gui,self.requestCameFrom)
                self.GETUSERINPUT_Response = Utility.ConvertToJson(guiResponse,self.requestCameFrom)
                self.GetUserInput_inputText = self.GETUSERINPUT_Response.get("GetUserInputResponse", {}).get("InputData")
        except Exception as e : self.ErrorText = f"Error in GETUSERINPUT: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def GCBTransaction(self, **kwargs) :
        """Handle GCB transaction and parse the response."""
        try :
            Gcb_Transaction_Req = self.Transaction_Request_Builder.GetCardBINRequest(**kwargs)
            GCB_Transaction_res = self.handleSocketRequest(Gcb_Transaction_Req, kwargs.get("bypassEnabled"),kwargs.get("getstatusEnabled"))
            if GCB_Transaction_res:
                try:
                    self.Gcb_Transaction_Request = Utility.ConvertToJson(Gcb_Transaction_Req,self.requestCameFrom)
                    self.Gcb_Transaction_Response = Utility.ConvertToJson(GCB_Transaction_res,self.requestCameFrom)
                    GcbResponse = self.Gcb_Transaction_Response.get(Utility.findNode(self.Gcb_Transaction_Response), {})
                    self.Gcb_Transaction_ResponseCode = GcbResponse.get("ResponseCode")
                    self.Gcb_Transaction_ResponseText = GcbResponse.get("ResponseText")
                    self.Gcb_Transaction_CardType = GcbResponse.get("CardType")
                    self.Gcb_Transaction_CashbackAmount = GcbResponse.get("CashBackAmount")
                    if self.Gcb_Transaction_ResponseCode and self.Gcb_Transaction_ResponseCode.startswith("0") :
                        self.Gcb_Transaction_CardToken = GcbResponse.get("CardToken")
                        if kwargs.get("LookUpFlag") in ["16", "8", "24"]:
                            self.Gcb_Transaction_CIToken = GcbResponse.get("ECOMMInfo", {}).get("CardIdentifier")
                            self.Gcb_Transaction_CRMToken = GcbResponse.get("CRMToken")
                        self.tokenForTransaction = {"01" : self.Gcb_Transaction_CardToken, "02" : self.Gcb_Transaction_CIToken, "03" : self.Gcb_Transaction_CRMToken}.get(kwargs.get("TransactionToken"), "")
                    if self.Gcb_Transaction_ResponseCode and (self.Gcb_Transaction_ResponseCode.startswith('3') or self.Gcb_Transaction_ResponseCode.startswith('6')):
                        self.CLOSETransaction()
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' }"; self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in GCBTransaction: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def ParentTransactionProcessing(self, **kwargs) :
        try :
            if self.Gcb_Transaction_ResponseCode is None or self.Gcb_Transaction_ResponseCode.startswith("0") :
                kwargs.update(RandomNumber=self.RandomNumberForInvoice, CardType=self.Gcb_Transaction_CardType, cashbackAmount=self.Gcb_Transaction_CashbackAmount, Token=self.tokenForTransaction)
                Parent_Transaction_req = self.Transaction_Request_Builder.Parent_Transaction(**kwargs)
                Parent_Transaction_res = self.handleSocketRequest(Parent_Transaction_req,"", "")
                if Parent_Transaction_res:
                    try :
                        self.Parent_Transaction_request = Utility.ConvertToJson(Parent_Transaction_req,self.requestCameFrom)
                        self.Parent_Transaction_response = Utility.ConvertToJson(Parent_Transaction_res,self.requestCameFrom)
                        ParentRequestNode = Utility.findNode(self.Parent_Transaction_request)
                        ParentResponseNode = Utility.findNode(self.Parent_Transaction_response)
                        TransType = self.Parent_Transaction_request.get(ParentRequestNode).get("TransactionType", )
                        trans_detail = self.Parent_Transaction_response.get(ParentResponseNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        self.Parent_Transaction_AurusPayTicketNum = self.Parent_Transaction_response.get(ParentResponseNode, {}).get("AurusPayTicketNum", "")
                        if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                        self.Parent_Transaction_ResponseCode = trans_detail.get("ResponseCode")
                        self.Parent_Transaction_ResponseText = trans_detail.get("ResponseText")
                        self.Parent_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier')
                        self.Parent_Transaction_TransactionAmount = trans_detail.get('TotalApprovedAmount')
                        self.ParentTransactionTypeName = "Sale" if TransType == "01" else "Pre-auth" if TransType == "04" else "Refund w/o Sale" if TransType == "02" else "Gift Transactions"
                        if kwargs.get("childTransactionType") != "76":
                            self.CLOSETransaction()
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' }"; self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in TransRequest: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText); self.CLOSETransaction()

    def ChildTransactionProcessing(self, **kwargs) :
        if self.Parent_Transaction_ResponseCode and self.Parent_Transaction_ResponseCode.startswith("0") :
            TransAmount = kwargs.get("TransactionAmount")
            TransactionType = kwargs.get("TransactionType")
            self.Parent_Transaction_TransactionAmount = self.Parent_Transaction_TransactionAmount if TransAmount is None else TransAmount
            Transactions = TransactionType.split("_")
            childTransactionType = Transactions[0]
            kwargs.update(RandomNumber=self.RandomNumberForInvoice, Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier,Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum,CardType=self.Gcb_Transaction_CardType, TransactionType=childTransactionType, TransactionAmount=self.Parent_Transaction_TransactionAmount)
            Child_Transaction = self.Transaction_Request_Builder.Child_Transaction(**kwargs)
            child_Transaction_res = self.handleSocketRequest(Child_Transaction,"", "")
            if child_Transaction_res:
                try:
                    self.Child_Transaction_request = Utility.ConvertToJson(Child_Transaction,self.requestCameFrom)
                    self.Child_Transaction_response = Utility.ConvertToJson(child_Transaction_res,self.requestCameFrom)
                    RequestTopnode = next(iter(self.Child_Transaction_request))
                    ResponseTopNode = next(iter(self.Child_Transaction_response))
                    TransType = self.Child_Transaction_request.get(RequestTopnode, {}).get("TransactionType")
                    trans_detail = self.Child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                    if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                    self.Child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                    self.Child_Transaction_ResponseCode= trans_detail.get("ResponseCode", "")
                    self.Child_Transaction_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                    self.Child_Transaction_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                    self.ChildTransactionTypeName = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
                    childOfChildTransactionType = Transactions[1] if len(Transactions) > 1 else None
                    if childOfChildTransactionType != "76":
                        self.CLOSETransaction()
                    if childOfChildTransactionType and self.Child_Transaction_ResponseCode.startswith("0"):
                        kwargs.update(RandomNumber=self.RandomNumberForInvoice, Parent_TransactionID=self.Child_Transaction_TransactionIdentifier,Parent_AurusPayTicketNum=self.Child_Transaction_AurusPayTicketNumber,CardType=self.Gcb_Transaction_CardType, TransactionType=childOfChildTransactionType, TransactionAmount=self.Parent_Transaction_TransactionAmount)
                        Child_of_child_Transaction = self.Transaction_Request_Builder.Child_Transaction(**kwargs)
                        Child_of_child_res = self.handleSocketRequest(Child_of_child_Transaction,"", "")
                        if Child_of_child_res:
                            self.Child_of_child_Transaction_request = Utility.ConvertToJson(Child_of_child_Transaction,self.requestCameFrom)
                            self.Child_of_child_Transaction_response = Utility.ConvertToJson(Child_of_child_res,self.requestCameFrom)
                            RequestTopnode = next(iter(self.Child_of_child_Transaction_request))
                            ResponseTopNode = next(iter(self.Child_of_child_Transaction_response))
                            TransType = self.Child_of_child_Transaction_request.get(RequestTopnode, {}).get("TransactionType")
                            trans_detail = self.Child_of_child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                            if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                            self.Child_of_child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                            self.Child_of_child_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                            self.Child_of_child_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                            self.ChildOfChildTransactionTypeName = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
                            self.CLOSETransaction()
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' }"; self.CLOSETransaction()

    def CLOSETransaction(self) :
        """Close the transaction."""
        try :
            closeTransRes = self.handleSocketRequest(self.Transaction_Request_Builder.CloseTransactionRequest(), "", "")
            if closeTransRes:
                closeData = Utility.ConvertToJson(closeTransRes,self.requestCameFrom)
                ResponseCode = closeData.get("CloseTransactionResponse").get("ResponseCode")
                if ResponseCode and not ResponseCode.startswith('0'):
                    self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in CLOSETransaction: {e}\nTraceback:\n{traceback.format_exc()}"