import configparser
import os
from Miejer_Petro.settings import BASE_DIR


class config :
    configData = configparser.RawConfigParser()
    configData.read(".\\Config.ini")

    @staticmethod
    def POSID() : return config.configData.get('AESDKParameter', 'POSID')

    @staticmethod
    def CCTID() : return config.configData.get('AESDKParameter', 'CCTID')

    @staticmethod
    def ADSDKSpecVer() : return config.configData.get('AESDKParameter', 'ADSDKSpecVer')

    @staticmethod
    def SessionId() : return config.configData.get('AESDKParameter', 'SessionId')

    @staticmethod
    def LanguageIndicator() : return config.configData.get('AESDKParameter', 'LanguageIndicator')

    @staticmethod
    def API_Delay(): return config.configData.get("Common", "API_DELAY")

    @staticmethod
    def commProtocol() : return config.configData.get('Common', 'WRAP_COMM_TYPE')

    @staticmethod
    def Config_machine_ip() : return config.configData.get('Common', 'SYSTEM_IP')

    @staticmethod
    def processor() : return config.configData.get('Common', 'PROCESSOR')

    @staticmethod
    def request_format() : return config.configData.get('Instore', 'REQUEST_FORMAT')

    @staticmethod
    def Outdoor_request_format() : return config.configData.get('Outdoor', 'REQUEST_FORMAT')

    @staticmethod
    def Instore_file_path() : return config.configData.get('Instore', 'FILE_PATH')

    @staticmethod
    def Outdoor_file_path() : return config.configData.get('Outdoor', 'FILE_PATH')

    @staticmethod
    def Config_Indoor_port() : return config.configData.get('Instore', 'POS_LISTENING_PORT')

    @staticmethod
    def Config_Outdoor_port() : return config.configData.get('Outdoor', 'POS_LISTENING_PORT')

    @staticmethod
    def xls_file_path() : return config.configData.get('Outdoor', 'XLS_FILE')

    @staticmethod
    def API_SEQUENCE() : return config.configData.get("Instore", "API_SEQUENCE")

    @staticmethod
    def OUTDOOR_API_SEQUENCE() : return config.configData.get("Outdoor", "API_SEQUENCE")

    @staticmethod
    def Full_Outdoor_file_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path())

    @staticmethod
    def Full_Indoor_file_path() : return os.path.join(BASE_DIR, config.Instore_file_path())

    @staticmethod
    def Full_xls_file_path() : return os.path.join(BASE_DIR, config.xls_file_path())

    @staticmethod
    def Indoor_xml_request_path() : return os.path.join(BASE_DIR, config.Instore_file_path() + "XML" + "\\")

    @staticmethod
    def Indoor_json_request_path() : return os.path.join(BASE_DIR, config.Instore_file_path() + "JSON" + "\\")

    @staticmethod
    def Outdoor_xml_request_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path() + "XML" + "\\")

    @staticmethod
    def Outdoor_json_request_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path() + "JSON" + "\\")