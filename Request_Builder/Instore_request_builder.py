import datetime
import json
import time
from decimal import Decimal, ROUND_HALF_UP

from API.Excel_operations import Excel_Operations
from API.Gift_Processor import Gift_processor
from API.Product_data_mapping import Product_data_mapping
from API.config import config


class Transaction_Request_Builder :

    def __init__(self) :
        self.request = None
        self.POSID = config.POSID()
        self.CCTID = config.CCTID()
        self.SessionId = config.SessionId()
        self.ADSDKSpecVer = config.ADSDKSpecVer()
        self.languageIndicator = config.LanguageIndicator()
        self.APPID = "01"
        self.TodaysDate = datetime.datetime.now().strftime('%m/%d/%Y').replace("/", "")
        self.currentTime = time.strftime("%H:%M:%S:%MS", time.localtime()).replace(":", "")[:-3]
        self.DefaultAmount = "10.00" #Decimal(Decimal((str(random.randint(0, 99)))).quantize(Decimal('1.00')))
        self.isXml = config.request_format().upper() == "XML"


    def InitAESDKRequest(self):
        data = Excel_Operations.readIndoorFile("InitAESDKRequest.txt")
        if data:
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def CCTTicketDisplayRequest(self, productCount) :
        data = Excel_Operations.readIndoorFile("CCTTicketDisplayRequest.txt")
        if data :
            data["CCTTicketDisplayRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "DisplayFlag" : "00",
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransTotalAmount" : str(self.DefaultAmount),
                "HeaderText" : "Please check Products"
            })
            if int(productCount) != 0 :
                products = Product_data_mapping.ProductData_Mapping(str(self.DefaultAmount), "", "TicketProductData", productCount)
                product_count = products['Product_count']
                product_list = products['Product_list']
                data["CCTTicketDisplayRequest"].update({
                    "TicketProductData" : {
                        "TicketCount" : "1",
                        "Tickets" : {
                            "Ticket" : {
                                "TicketNumber" : "001",
                                "ProductCount" : str(product_count),
                                "Products" : {
                                    "Product" : list(product_list)
                                }
                            }
                        }
                    }
                })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetStatusRequest(self, Type) :
        data = Excel_Operations.readIndoorFile("GetStatusRequest.txt")
        if data :
            data["GetStatusRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "StatusType" : Type
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def SignatureRequest(self) :
        data = Excel_Operations.readIndoorFile("SignatureRequest.txt")
        if data :
            data["SignatureRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,

            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def RestartCCTRequest(self):
        data = Excel_Operations.readIndoorFile("RestartCCTRequest.txt")
        if data:
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetCardBINRequest(self, Transaction_type, AllowKeyedEntry, EntrySource, LookUpFlag) :
        data = Excel_Operations.readIndoorFile("GetCardBINRequest.txt")
        if data :
            TransactionTypeToRequest = Transaction_type
            data["GetCardBINRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "languageIndicator" : self.languageIndicator,
                "MessageLine1" : ("Sale" if TransactionTypeToRequest == "01" else "Pre-auth" if TransactionTypeToRequest == "04" else "Refund w/o Sale" if TransactionTypeToRequest == "02" else "Gift" if TransactionTypeToRequest in ("11", "12", "16", "18") else "" )+" Transaction",
                "TransactionType" : TransactionTypeToRequest if TransactionTypeToRequest == "02" else "",
                "TenderAmount" : self.DefaultAmount,
                "AllowKeyedEntry" : AllowKeyedEntry,
                "EntrySource" : EntrySource,
                "LookUpFlag" : LookUpFlag,
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ShowScreenRequest(self, message, message2, flag) :
        data = Excel_Operations.readIndoorFile("ShowScreenRequest.txt")
        if data :
            data["ShowScreenRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "MessageLine1" : message,
                "MessageLine2" : message2,
                "ActivityFlag" : flag
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ShowListRequest(self, OptionsType) :
        data = Excel_Operations.readIndoorFile("ShowListRequest.txt")
        if data :
            data["ShowListRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "OptionsType" : OptionsType
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetUserInputRequest(self, message, option) :
        data = Excel_Operations.readIndoorFile("GetUserInputRequest.txt")
        if data :
            data["GetUserInputRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "HeaderText" : message,
                "Type" : option
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ByPassScreenRequest(self, ByPassOptions) :
        data = Excel_Operations.readIndoorFile("ByPassScreenRequest.txt")
        if data :
            data["ByPassScreenRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "ByPassOptions" : str(ByPassOptions)
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def Parent_Transaction(self,AllowKeyedEntry, Token_type, TransactionTypeID, Token, CardType, productCount, RandomNumber, TransAmount, cashbackAmount) :
        data = Excel_Operations.readIndoorFile("TransRequest.txt")
        if data :
            Token_type = Token_type if Token_type is not None else ""
            Token = Token if Token is not None else ""
            CardType = CardType if CardType is not None else ""
            TransactionTypeToRequest =  TransactionTypeID
            TransAmount = str(TransAmount) if TransAmount is not None else str(self.DefaultAmount)
            rounded_value = str((Decimal(TransAmount) / 4).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            EntrySource = "K" if AllowKeyedEntry.upper() == "Y" else ""
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                "EntrySource" : EntrySource,
                **(
                    {"SubTransType" : "04" if TransactionTypeToRequest in ("16", "18") else "",
                     "BlackHawkUpc" : Gift_processor.BlackHawkUpc_finder(Token),
                     "ProgramId" : "11" if CardType.upper().endswith("P") else "",
                     } if CardType.upper().startswith("GC") else {}
                ),
                **(
                    {"CardToken" : Token} if Token_type == "01" else
                    {"CRMToken" : Token} if Token_type == "03" else
                    {"ECOMMInfo" : {"CardIdentifier" : Token} if Token_type == "02" else {}}
                ),
                "ReferenceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
            })
            TransAmountDetails.update({
                "TransactionTotal" : TransAmount,
                "TenderAmount" : TransAmount,
                **({"EbtAmount" : TransAmount} if CardType.upper() == "EBF" else {}),
                **({'PrescriptionAmount' : rounded_value,
                    'CoPaymentAmount' : rounded_value,
                    'DentalAmount' : rounded_value,
                    'VisionOpticalAmount' : rounded_value,
                    'HealthCareAmount' : TransAmount,
                    'FSAAmount' : TransAmount} if CardType.upper().endswith("S") else {})
            })
            if int(productCount) != 0 and not CardType.upper().endswith("S") :
                if config.processor().upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(TransAmount, cashbackAmount, "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if config.processor().upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(TransAmount, cashbackAmount, "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}}})
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def Child_Transaction(self, RandomNumber, TransactionTypeID, Parent_TransactionID, Parent_AurusPayTicketNum, CardType, productCount, Transaction_total) :
        FileName = "CancelLastTransRequest" if TransactionTypeID.upper() == "76" else "ChildTransRequest"
        data = Excel_Operations.readIndoorFile(FileName + ".txt")
        if data :
            CardType = "XXC" if CardType is None else CardType
            TransactionTypeToRequest =  TransactionTypeID
            Child = data["CancelLastTransRequest"] if TransactionTypeToRequest.upper() == "76" else data["TransRequest"]
            Child.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                **({
                       "ReferenceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                       "InvoiceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}",
                       "OrigTransactionIdentifier" : Parent_TransactionID,
                       "OrigAurusPayTicketNum" : Parent_AurusPayTicketNum,
                       "TransactionDate" : self.TodaysDate,
                       "TransactionTime" : self.currentTime,
                       "TransAmountDetails" : {
                           "TransactionTotal" : Transaction_total,
                           "TenderAmount" : Transaction_total,
                       }
                   } if TransactionTypeToRequest.upper() != "76" else
                   {
                       "Date" : self.TodaysDate,
                       "Time" : self.currentTime
                   }), #cancellast check
            })

            if int(productCount) != 0 and TransactionTypeToRequest.upper() in ("02", "05"):
                if config.processor().upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(Transaction_total,"", "l3productdata", productCount)
                    Child.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if config.processor().upper() == "FD" or CardType.endswith("F") :
                    products = Product_data_mapping.ProductData_Mapping(Transaction_total,"", "fleetproductdata", productCount)
                    Child.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}
                             }
                })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def CloseTransactionRequest(self) :
        data = Excel_Operations.readIndoorFile("CloseTransactionRequest.txt")
        if data :
            CloseTransactionRequest = data["CloseTransactionRequest"]
            CloseTransactionRequest.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
            })
            self.request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request