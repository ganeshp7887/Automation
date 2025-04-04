import datetime
import json
import time
from decimal import Decimal, ROUND_HALF_UP

from API.Utility import Utility
from API.Gift_Processor import Gift_processor
from API.Product_data_mapping import Product_data_mapping
from API.configfile import configFile as cn

class Transaction_Request_Builder :

    @staticmethod
    def readIndoorFile(filename) :
        file_path = rf"{cn().Full_Indoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    def __init__(self) :
        config = cn()
        self.request = None
        self.POSID = config.POSID()
        self.CCTID = config.CCTID()
        self.SessionId = config.SessionId()
        self.ADSDKSpecVer = config.ADSDKSpecVer()
        self.languageIndicator = config.LanguageIndicator()
        self.processor = config.processor()
        self.APPID = "01"
        self.TodaysDate = datetime.datetime.now().strftime('%m/%d/%Y').replace("/", "")
        self.currentTime = time.strftime("%H:%M:%S:%MS", time.localtime()).replace(":", "")[:-3]
        self.DefaultAmount = "10.00" #Decimal(Decimal((str(random.randint(0, 99)))).quantize(Decimal('1.00')))
        self.isXml = config.request_format().upper() == "XML"

    def InitAESDKRequest(self):
        data = self.readIndoorFile("InitAESDKRequest.txt")
        if data:
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def CCTTicketDisplayRequest(self, productCount) :
        data = self.readIndoorFile("CCTTicketDisplayRequest.txt")
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
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetStatusRequest(self) :
        data = self.readIndoorFile("GetStatusRequest.txt")
        if data :
            data["GetStatusRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def SignatureRequest(self) :
        data = self.readIndoorFile("SignatureRequest.txt")
        if data :
            data["SignatureRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,

            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def RestartCCTRequest(self):
        data = self.readIndoorFile("RestartCCTRequest.txt")
        if data:
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetCardBINRequest(self, **kwargs) :
        data = self.readIndoorFile("GetCardBINRequest.txt")
        TransactionType, AllowKeyedEntry, EntrySource,LookUpFlag, TransactionAmount = kwargs.get("TransactionType"), kwargs.get("AllowKeyedEntry"), kwargs.get("EntrySource"), kwargs.get("LookUpFlag"), kwargs.get("TransactionAmount")
        if data :
            data["GetCardBINRequest"].update({
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "languageIndicator" : self.languageIndicator,
                "MessageLine1" : ("Sale" if TransactionType == "01" else "Pre-auth" if TransactionType == "04" else "Refund w/o Sale" if TransactionType == "02" else "Gift" if TransactionType in ("11", "12", "16", "18") else "" )+" Transaction",
                "TransactionType" : TransactionType if TransactionType == "02" else "",
                "TenderAmount" : str(TransactionAmount) if TransactionAmount else self.DefaultAmount,
                "AllowKeyedEntry" : AllowKeyedEntry,
                "EntrySource" : EntrySource,
                "LookUpFlag" : LookUpFlag,
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ShowScreenRequest(self, message, message2, flag) :
        data = self.readIndoorFile("ShowScreenRequest.txt")
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
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ShowListRequest(self, OptionsType) :
        data = self.readIndoorFile("ShowListRequest.txt")
        if data :
            data["ShowListRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "OptionsType" : OptionsType
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def GetUserInputRequest(self, message, option) :
        data = self.readIndoorFile("GetUserInputRequest.txt")
        if data :
            data["GetUserInputRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "HeaderText" : message,
                "Type" : str(option)
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def ByPassScreenRequest(self, ByPassOptions) :
        data = self.readIndoorFile("ByPassScreenRequest.txt")
        if data :
            data["ByPassScreenRequest"].update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "ByPassOptions" : str(ByPassOptions)
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def Parent_Transaction(self, **kwargs) :
        data = self.readIndoorFile("TransRequest.txt")
        if data :
            TransactionToken = kwargs.get("TransactionToken", "")
            Token = kwargs.get("Token", "")
            CardType = "XXC" if  kwargs.get("CardType") is None else kwargs.get("CardType")
            TransactionTypeToRequest = kwargs.get("TransactionType", "")
            TransAmount = kwargs.get("TransactionAmount", None) if kwargs.get("TransactionAmount") else str(self.DefaultAmount)
            productCount = kwargs.get("ProductCount", 0)
            RandomNumber = kwargs.get("RandomNumber", 0)
            cashbackAmount = kwargs.get("cashbackAmount", "")
            rounded_value = str((Decimal(TransAmount) / 4).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                **(
                    {"SubTransType" : "04" if TransactionTypeToRequest in ("16", "18") else "",
                     "BlackHawkUpc" : Gift_processor.BlackHawkUpc_finder(Token),
                     "ProgramId" : "11" if CardType.upper().endswith("P") else "",
                     } if CardType.upper().startswith("GC") else {}
                ),
                **(
                    {"CardToken" : Token} if TransactionToken == "01" else
                    {"CRMToken" : Token} if TransactionToken == "03" else
                    {"ECOMMInfo" : {"CardIdentifier" : Token} if TransactionToken == "02" else {}}
                ),
                "ReferenceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{RandomNumber}{self.currentTime}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
            })
            TransAmountDetails.update({
                "TransactionTotal" : TransAmount,
                "TenderAmount" : TransAmount,
                **({"EBTAmount" : TransAmount} if CardType.upper() == "EBF" else {}),
                **({'PrescriptionAmount' : rounded_value,
                    'CoPaymentAmount' : rounded_value,
                    'DentalAmount' : rounded_value,
                    'VisionOpticalAmount' : rounded_value,
                    'HealthCareAmount' : TransAmount,
                    'FSAAmount' : TransAmount} if CardType.upper().endswith("S") else {})
            })
            if int(productCount) != 0 and not CardType.upper().endswith("S") :
                if self.processor.upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(TransAmount, cashbackAmount, "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if self.processor.upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(TransAmount, cashbackAmount, "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}}})
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def Child_Transaction(self, **kwargs) :
        TransactionType = kwargs.get("TransactionType")
        FileName = "CancelLastTransRequest" if TransactionType.upper() == "76" else "ChildTransRequest"
        data = self.readIndoorFile(FileName + ".txt")
        if data :
            CardType = "XXC" if  kwargs.get("CardType") is None else kwargs.get("CardType")
            RandomNumber = kwargs.get("RandomNumber")
            Parent_TransactionID = kwargs.get("Parent_TransactionID")
            Parent_AurusPayTicketNum =kwargs.get("Parent_AurusPayTicketNum")
            TransactionAmount = kwargs.get("TransactionAmount")
            productCount = kwargs.get("ProductCount")
            TransactionTypeToRequest =  TransactionType
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
                           "TransactionTotal" : TransactionAmount,
                           "TenderAmount" : TransactionAmount,
                       }
                   } if TransactionTypeToRequest.upper() != "76" else
                   {
                       "Date" : self.TodaysDate,
                       "Time" : self.currentTime
                   }), #cancellast check
            })

            if int(productCount) != 0 and TransactionTypeToRequest.upper() in ("02", "05"):
                if self.processor.upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(TransactionAmount,"", "l3productdata", productCount)
                    Child.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if self.processor.upper() == "FD" or CardType.endswith("F") :
                    products = Product_data_mapping.ProductData_Mapping(TransactionAmount,"", "fleetproductdata", productCount)
                    Child.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}
                             }
                })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request

    def CloseTransactionRequest(self) :
        data = self.readIndoorFile("CloseTransactionRequest.txt")
        if data :
            CloseTransactionRequest = data["CloseTransactionRequest"]
            CloseTransactionRequest.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "CCTID" : self.CCTID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
            })
            self.request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.request