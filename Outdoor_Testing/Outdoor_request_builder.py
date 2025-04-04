import datetime
import json
import time

from API.Utility import Utility
from API.Fleet_Processor import fleet_processor, fleet_data_appender
from API.Gift_Processor import Gift_processor
from API.Product_data_mapping import Product_data_mapping
from API.configfile import configFile as cn


class Outdoor_Request_Builder :

    @staticmethod
    def readOutdoorFile(filename) :
        file_path = rf"{cn().Full_Outdoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    def __init__(self) :
        config = cn()
        self.Request = None
        self.POSID = config.POSID()
        self.CCTID = config.CCTID()
        self.SessionId = config.SessionId()
        self.ADSDKSpecVer = config.ADSDKSpecVer()
        self.Processor = config.processor()
        self.APPID = "01"
        self.defaultAmount = "10.00"
        self.TodaysDate = datetime.datetime.now().strftime('%m/%d/%Y').replace("/", "")
        self.YYMMDD = datetime.datetime.now().strftime('%y/%m/%d').replace("/", "")
        self.currentTime = time.strftime("%H:%M:%S:%MS", time.localtime()).replace(":", "")[:-3]
        self.RandomNumber = 123456
        self.isXml = config.Outdoor_request_format().upper() == "XML"


    def gcb(self, **kwargs) :
        data = self.readOutdoorFile("GetCardBINRequest.txt")
        if data :
            data["GetCardBINRequest"].update({
                "POSID" : self.POSID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "LookUpFlag" : kwargs.get("LookUpFlag"),
                "CardDataInfo" : {
                    "CardDataSource" :kwargs.get("CardDataSource"),
                    "EncryptionMode" : kwargs.get("EncryptionMode"),
                    "TrackData" : kwargs.get("TrackData"),
                    "EMVDetailsData" : kwargs.get("EMVDetailsData"),
                    "PINBlock" : kwargs.get("PINBlock"),
                    "KSNBlock" : kwargs.get("KSNBlock"),
                    "PinBlockMode" : kwargs.get("PinBlockMode"),
                }
            })
            self.Request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request

    def Parent_Transaction(self, **kwargs) :
        data = self.readOutdoorFile("parentTransRequest.txt")
        if data :
            TransactionTypeToRequest = kwargs.get("TransactionType")
            productCount = kwargs.get("product_count")
            TrackData = kwargs.get("TrackData")
            CardDataSource = kwargs.get("CardDataSource")
            defaultAmount = self.defaultAmount if kwargs.get("Transaction_total") is ["", None] else kwargs.get("Transaction_total")
            print(f"Amount in request default:: {defaultAmount}")
            CardType = "VIC" if kwargs.get("CardType") is None else kwargs.get("CardType")
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                "TransactionSequenceNumber" : str(kwargs.get("TransactionSeqNum")).zfill(6),
                "CRMToken" : TrackData if TransactionTypeToRequest == "22" else "",
                **(
                    {
                        "SubTransType" : "04" if TransactionTypeToRequest in ("16", "11") else "",
                        "BlackHawkUpc" : Gift_processor.BlackHawkUpc_finder(fleet_processor.cardnumber_finder(TrackData, CardDataSource)),
                        "ProgramId" : "11" if CardType.upper().endswith("P") else "",
                    } if CardType.upper().startswith("GC") else {}
                ),
                "CardType" : CardType,
                **(
                    {"CardDataInfo" :
                        {
                            "CardDataSource" : CardDataSource,
                            "EncryptionMode" : kwargs.get("EncryptionMode"),
                            "TrackData" : TrackData,
                            "EMVDetailsData" : kwargs.get("EMVDetailsData"),
                            "PINBlock" : kwargs.get("PINBlock"),
                            "KSNBlock" : kwargs.get("KSNBlock"),
                            "PinBlockMode" : kwargs.get("PinBlockMode"),
                        }
                    } if TransactionTypeToRequest != "02" else {}
                ),
                "ReferenceNumber" : f"{self.TodaysDate}{self.currentTime}{self.RandomNumber}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{self.currentTime}{self.RandomNumber + 1}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
            })
            TransAmountDetails.update({
                "TransactionTotal" : defaultAmount,
                "TenderAmount" : defaultAmount,
            })
            if int(productCount) != 0 and TransactionTypeToRequest not in "09" and not CardType.upper().endswith("S") :
                if self.Processor.upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(defaultAmount, "", "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if self.Processor.upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(defaultAmount, "", "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}}})
            if CardType.endswith('F') and TransactionTypeToRequest.upper() not in ["09", "02"] :
                prompts = fleet_processor.Track_data_prompt_finder(TrackData, CardDataSource, CardType)
                cnumber = fleet_processor.cardnumber_finder(TrackData, CardDataSource)
                prompts_appender = fleet_data_appender.Prompt_finder_by_value(prompts, CardType, cnumber)
                Parent.update({
                    "FleetPromptsData" : prompts_appender
                })
            self.Request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request

    def Child_Transaction(self, **kwargs) :
        data = self.readOutdoorFile("childTransRequest.txt")
        if data:
            TransactionTypeToRequest = kwargs.get("TransactionType")
            CardType =  kwargs.get("CardType")
            TransAmount = kwargs.get("TransAmount")
            DuplicateTransCheck = kwargs.get("DuplicateTransCheck")
            productCount = kwargs.get("product_count")
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                "TransactionSequenceNumber" : str(kwargs.get("TransactionSeqNum")).zfill(6),
                "ReferenceNumber" : f"{self.TodaysDate}{self.RandomNumber}{self.currentTime}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{self.RandomNumber}{self.currentTime}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
                "OrigTransactionIdentifier" : kwargs.get("Parent_TransactionID"),
                "OrigAurusPayTicketNum" : kwargs.get("Parent_AurusPayTicketNum"),
                "DuplicateTransCheck" : DuplicateTransCheck,
                "OfflineTicketNumber" : f"O{self.YYMMDD}12345678001" if DuplicateTransCheck == "1" else ""
            })
            TransAmountDetails.update({
                "TransactionTotal" :TransAmount if TransactionTypeToRequest.upper() == "06" else self.defaultAmount,
                "TenderAmount" : TransAmount if TransactionTypeToRequest.upper() == "06" else self.defaultAmount
            })
            if productCount and int(productCount) != 0 and TransactionTypeToRequest in ("05", "02") and not CardType.upper().endswith("S") :
                if self.Processor.upper() == "CHASE" and (CardType.endswith("D") or CardType.endswith("C")) :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if self.Processor.upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}
                             }
                    })
            self.Request = Utility.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request