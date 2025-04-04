import socket
import time
import requests
from API.configfile import configFile
from decimal import Decimal
import json

class Adsdk_Socket:

    def __init__(self):
        config = configFile()
        self.sock = None
        self.ip = config.system_ip()
        self.port = config.Config_Indoor_port()
        self.instoreRequestFormat = config.request_format()
        self.outdoorRequestFormat = config.Outdoor_request_format()
        self.outdoorPort = config.Config_Outdoor_port()
        self.response = None
        self.httpsResponse = None
        self.delay = Decimal(Decimal(config.API_Delay()).quantize(Decimal("1.000")))
        self.isHttps = config.commProtocol() != "5"

    def handleSocketRequest(self, request_data, requestFrom) :
        IP = self.ip
        PORT = self.port
        RequestFormat = "XML"
        if requestFrom.upper() == "INSTORE":
            PORT = self.port
            RequestFormat = self.instoreRequestFormat
        if requestFrom.upper() == "OUTDOOR":
            PORT = self.outdoorPort
            RequestFormat = self.outdoorRequestFormat

        isXml = RequestFormat.upper() == "XML"

        if not isXml : request_data = json.loads(request_data)
        if self.isHttps :
            try :
                self.openSocket(port=PORT)
                try :
                    self.sendRequest(str(request_data))
                    try :
                        response = self.receiveResponseFromSocket()
                        return response
                    except Exception as e :
                        self.ErrorText = f"Response not received from @ {IP}::{PORT} ==> {e}"
                except Exception as e :
                    self.ErrorText = f"Request send Fails @ {IP}::{PORT} ==> {e}"
            except Exception as e :
                self.ErrorText = f"Connection Fails @ {IP}::{PORT} ==> {e}"
        else :
            try :
                url = f"https://{IP}:{PORT}"
                self.httpsRequest(url, request_data, RequestFormat.lower())
                try :
                    response = self.receiveResponsehttps()
                    return response
                except Exception as e :
                    self.ErrorText = f"Received response Fails @ {IP}::{PORT} ==> {e}"
            except Exception as e :
                self.ErrorText = f"Connection Fails @ {IP}::{PORT} ==> {e}"

    def openSocket(self, port):
        server_address = (self.ip, int(port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)

    def sendRequest(self, request):
      #  print(f"Request send :: {request}")
        self.sock.sendall(request.encode('utf-8'))

    def receiveResponseFromSocket(self):
        buf = bytearray()
        while True:
            chunk = self.sock.recv(12288)
            if not chunk:
                break
            buf.extend(chunk)
        #    print(f"Response Rec :: {buf.decode('utf-8')}")
            time.sleep(float(self.delay))
            return buf.decode('utf-8')

    def httpsRequest(self, url, request, requestFormat):
        print(f"Request send :: {request}")
        headers = {"Content-Type": f"application/json"}
        self.httpsResponse  = requests.post(url, json=request, verify=False, headers=headers).text

    def receiveResponsehttps(self):
        print(f"Response Rec :: {self.httpsResponse}")
        time.sleep(float(self.delay))
        return self.httpsResponse

    def closeSocket(self): self.sock.close()