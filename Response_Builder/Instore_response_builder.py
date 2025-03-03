import json
import random
import threading
import time
import traceback
from API.Excel_operations import Excel_Operations
from API.Socket_API import Adsdk_Socket as socket
from API.config import config
from Request_Builder.Instore_request_builder import Transaction_Request_Builder

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
        self.port = config.Config_Indoor_port()
        self.OutdoorPort = config.Config_Outdoor_port()
        self.Transaction_Request_Builder = Transaction_Request_Builder()
        self.ip = config.Config_machine_ip()
        self.urlExtension = ""
        self.APIurl = ""
        self.url = rf"https://{self.ip}:{self.port}{self.urlExtension}{self.APIurl}"
        self.socket = socket()
        self.isHttps = config.commProtocol() != "5"
        self.isXml = config.request_format().upper() == "XML"
        self.isSignatureEnabled = "0"
        self.ChildTransactionType = None
        self.ChildOfChildTransactionType = None
        self.ErrorText = None
        self.tokenForTransaction = ""
        self.ParentTransactionTypeName = None
        self.ChildTransactionTypeName = None
        self.ChildOfChildTransactionTypeName = None

    def handleSocketRequest(self, request_data) :
        if not self.isXml: request_data = json.loads(request_data)
        if self.isHttps :
            try:
                self.socket.openSocket(port=self.port)
                try:
                    self.socket.sendRequest(str(request_data))
                    try:
                        response = self.socket.receiveResponseFromSocket()
                        return response
                    except Exception as e:
                        self.ErrorText = f"Response not received from @ {self.ip}::{self.port} ==> {e}"
                except Exception as e:
                    self.ErrorText = f"Request send Fails @ {self.ip}::{self.port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Connection Fails @ {self.ip}::{self.port} ==> {e}"
        else :
            try:
                self.socket.httpsRequest(self.url, request_data, config.request_format().lower())
                try:
                    response = self.socket.receiveResponsehttps()
                    return response
                except Exception as e:
                    self.ErrorText = f"Received response Fails @ {self.ip}::{self.port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Connection Fails @ {self.ip}::{self.port} ==> {e}"

    def GetStatusRequest(self, RequestType) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.GetStatusRequest(RequestType))
        except Exception as e: self.ErrorText = f"Error in GetStatusRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def RestartCCTRequestTransaction(self):
        try : self.handleSocketRequest(self.Transaction_Request_Builder.RestartCCTRequest(), "", "")
        except Exception as e: self.ErrorText = f"Error in RestartCCTRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def Signature(self) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.SignatureRequest())
        except Exception as e: self.ErrorText = f"Error in Signature: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def displayTicket(self, productCount) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.CCTTicketDisplayRequest(productCount))
        except Exception as e: self.ErrorText = f"Error in displayTicket: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWLIST(self, OptionsType) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ShowListRequest(OptionsType))
        except Exception as e :   self.ErrorText = f"Error in SHOWLIST: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def BYPASSTransaction(self, bypassoption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ByPassScreenRequest(bypassoption))
        except Exception as e :  self.ErrorText = f"Error in Bypass: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWSCREEN(self, message, flag) :
        try :
            message2 = self.GetUserInput_inputText if self.GetUserInput_inputText else ""
            self.handleSocketRequest(self.Transaction_Request_Builder.ShowScreenRequest(str(message), str(message2), flag))
        except Exception as e : self.ErrorText = f"Error in SHOWSCREEN: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def GETUSERINPUT(self, message, option) :
        """Get user input."""
        try :
            gui = self.Transaction_Request_Builder.GetUserInputRequest(message, option)
            guiResponse = self.handleSocketRequest(gui)
            if guiResponse:
                self.GETUSERINPUT_Request = Excel_Operations.ConvertToJson(gui, self.isXml)
                self.GETUSERINPUT_Response = Excel_Operations.ConvertToJson(guiResponse, self.isXml)
                self.GetUserInput_inputText = self.GETUSERINPUT_Response.get("GetUserInputResponse", {}).get("InputData")
        except Exception as e : self.ErrorText = f"Error in GETUSERINPUT: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def GCBTransaction(self, **kwargs) :
        """Handle GCB transaction and parse the response."""
        try :
            Gcb_Transaction_Req = self.Transaction_Request_Builder.GetCardBINRequest(**kwargs)
            GCB_Transaction_res = self.handleSocketRequest(Gcb_Transaction_Req)
            if GCB_Transaction_res:
                try:
                    self.Gcb_Transaction_Request = Excel_Operations.ConvertToJson(Gcb_Transaction_Req, self.isXml)
                    self.Gcb_Transaction_Response = Excel_Operations.ConvertToJson(GCB_Transaction_res, self.isXml)
                    GcbResponse = self.Gcb_Transaction_Response.get(Excel_Operations.findNode(self.Gcb_Transaction_Response), {})
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
                    else:
                        self.CLOSETransaction()
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"; self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in GCBTransaction: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def ParentTransactionProcessing(self, **kwargs) :
        try :
            if self.Gcb_Transaction_ResponseCode is None or self.Gcb_Transaction_ResponseCode.startswith("0") :
                kwargs.update(RandomNumber=self.RandomNumberForInvoice, CardType=self.Gcb_Transaction_CardType, cashbackAmount=self.Gcb_Transaction_CashbackAmount, Token=self.tokenForTransaction)
                Parent_Transaction_req = self.Transaction_Request_Builder.Parent_Transaction(**kwargs)
                Parent_Transaction_res = self.handleSocketRequest(Parent_Transaction_req)
                if Parent_Transaction_res:
                    try :
                        self.Parent_Transaction_request = Excel_Operations.ConvertToJson(Parent_Transaction_req, self.isXml)
                        self.Parent_Transaction_response = Excel_Operations.ConvertToJson(Parent_Transaction_res, self.isXml)
                        ParentRequestNode = Excel_Operations.findNode(self.Parent_Transaction_request)
                        ParentResponseNode = Excel_Operations.findNode(self.Parent_Transaction_response)
                        TransType = self.Parent_Transaction_request.get(ParentRequestNode).get("TransactionType", )
                        trans_detail = self.Parent_Transaction_response.get(ParentResponseNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        self.Parent_Transaction_AurusPayTicketNum = self.Parent_Transaction_response.get(ParentResponseNode, {}).get("AurusPayTicketNum", "")
                        if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                        self.Parent_Transaction_ResponseCode = trans_detail.get("ResponseCode")
                        self.Parent_Transaction_ResponseText = trans_detail.get("ResponseText")
                        self.Parent_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier')
                        self.Parent_Transaction_TransactionAmount = trans_detail.get('TotalApprovedAmount')
                        self.ParentTransactionTypeName = "Sale" if TransType == "01" else "Pre-auth" if TransType == "04" else "Refund w/o Sale" if TransType == "02" else "Gift Transactions"
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"; self.CLOSETransaction()
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
            child_Transaction_res = self.handleSocketRequest(Child_Transaction)
            if child_Transaction_res:
                try:
                    self.Child_Transaction_request = Excel_Operations.ConvertToJson(Child_Transaction, self.isXml)
                    self.Child_Transaction_response = Excel_Operations.ConvertToJson(child_Transaction_res, self.isXml)
                    RequestTop_node = next(iter(self.Child_Transaction_request))
                    ResponseTopNode = next(iter(self.Child_Transaction_response))
                    TransType = self.Child_Transaction_request.get(RequestTop_node, {}).get("TransactionType")
                    trans_detail = self.Child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                    if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                    self.Child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                    self.Child_Transaction_ResponseCode= trans_detail.get("ResponseCode", "")
                    self.Child_Transaction_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                    self.Child_Transaction_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                    self.ChildTransactionTypeName = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
                    childOfChildTransactionType = Transactions[1] if len(Transactions) > 1 else None
                    if childOfChildTransactionType and self.Child_Transaction_ResponseCode.startswith("0"):
                        kwargs.update(RandomNumber=self.RandomNumberForInvoice, Parent_TransactionID=self.Child_Transaction_TransactionIdentifier,Parent_AurusPayTicketNum=self.Child_Transaction_AurusPayTicketNumber,CardType=self.Gcb_Transaction_CardType, TransactionType=childOfChildTransactionType, TransactionAmount=self.Parent_Transaction_TransactionAmount)
                        Child_of_child_Transaction = self.Transaction_Request_Builder.Child_Transaction(**kwargs)
                        Child_of_child_res = self.handleSocketRequest(Child_of_child_Transaction)
                        if Child_of_child_res:
                            self.Child_of_child_Transaction_request = Excel_Operations.ConvertToJson(Child_of_child_Transaction, self.isXml)
                            self.Child_of_child_Transaction_response = Excel_Operations.ConvertToJson(Child_of_child_res, self.isXml)
                            RequestTop_node = Excel_Operations.findNode(self.Child_of_child_Transaction_request)
                            ResponseTopNode = Excel_Operations.findNode(self.Child_of_child_Transaction_response)
                            TransType = self.Child_of_child_Transaction_request.get(RequestTop_node, {}).get("TransactionType")
                            trans_detail = self.Child_of_child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                            if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                            self.Child_of_child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                            self.Child_of_child_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                            self.Child_of_child_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                            self.ChildOfChildTransactionTypeName = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"; self.CLOSETransaction()


    def CLOSETransaction(self) :
        """Close the transaction."""
        try :
            closeTransRes = self.handleSocketRequest(self.Transaction_Request_Builder.CloseTransactionRequest())
            if closeTransRes:
                closeData = Excel_Operations.ConvertToJson(closeTransRes, self.isXml)
                ResponseCode = closeData.get("CloseTransactionResponse").get("ResponseCode")
                if ResponseCode and not ResponseCode.startswith('0'):
                    self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in CLOSETransaction: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText)