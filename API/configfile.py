import os
from Miejer_Petro.settings import BASE_DIR
import configparser

class configFile :

    @staticmethod
    def read_config() :
        config = configparser.RawConfigParser()
        config.read('.\\config.ini')
        return config

    def __init__(self):
        self.configData = self.read_config()

    def POSID(self) : return self.configData.get('AESDKParameter','POSID')

    def CCTID(self) : return self.configData.get('AESDKParameter','CCTID')

    def ADSDKSpecVer(self) : return self.configData.get('AESDKParameter','ADSDKSpecVer')

    def SessionId(self) : return self.configData.get('AESDKParameter','SessionId')

    def LanguageIndicator(self) : return self.configData.get('AESDKParameter','LanguageIndicator')

    def system_ip(self) :  return self.configData.get('Common','machineIP')

    def API_Delay(self): return self.configData.get('Common',"API_DELAY")

    def commProtocol(self) : return self.configData.get('Common','WRAP_COMM_TYPE')

    def processor(self) : return self.configData.get('Common','PROCESSOR')

    def request_format(self) : return self.configData.get('Instore','REQUEST_FORMAT')

    def Outdoor_request_format(self) : return self.configData.get('Outdoor','REQUEST_FORMAT')

    def Instore_file_path(self) : return self.configData.get('Instore','FILE_PATH')

    def Outdoor_file_path(self) : return self.configData.get('Outdoor','FILE_PATH')

    def Config_Indoor_port(self) : return self.configData.get('Instore','POS_LISTENING_PORT')

    def Config_Outdoor_port(self) : return self.configData.get('Outdoor','POS_LISTENING_PORT')

    def xls_file_path(self) : return self.configData.get('Outdoor','XLS_FILE')

    def API_SEQUENCE(self) : return self.configData.get('Instore',"API_SEQUENCE")

    def OUTDOOR_API_SEQUENCE(self) : return self.configData.get('Outdoor',"API_SEQUENCE")

    def Full_Outdoor_file_path(self) : return os.path.join(BASE_DIR, configFile.Outdoor_file_path(self))

    def Full_Indoor_file_path(self) : return os.path.join(BASE_DIR, configFile.Instore_file_path(self))

    def Full_xls_file_path(self) : return os.path.join(BASE_DIR, configFile.xls_file_path(self))

    def Indoor_xml_request_path(self) : return os.path.join(BASE_DIR, configFile.Instore_file_path(self) + "XML" + "\\")

    def Indoor_json_request_path(self) : return os.path.join(BASE_DIR, configFile.Instore_file_path(self) + "JSON" + "\\")

    def Outdoor_xml_request_path(self) : return os.path.join(BASE_DIR, configFile.Outdoor_file_path(self) + "XML" + "\\")

    def Outdoor_json_request_path(self) : return os.path.join(BASE_DIR, configFile.Outdoor_file_path(self) + "JSON" + "\\")