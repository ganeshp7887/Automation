import json
import re
import dict2xml
from django.http import JsonResponse
from django.shortcuts import render
from API.configfile import configFile
from Outdoor_Testing.Outdoor_response_builder import Transaction_Processing
from .models import OutdoorModel
from API.Utility import Utility


class OutdoorTesting:

    def __init__(self):
        self.result = {
            "Transactions" : Utility.readTransactionTypes().get("Outdoor_Transactions"),
        }

    def Outdoor_Testing(self, request):
        if request.method == 'POST':
            TransactionProcessing = OutdoorModel()
            result = TransactionProcessing.TransactionProcessing(request, isSingle=False)
            self.result.update(result)
            return JsonResponse(self.result, safe=False)
        else:
            return render(request, "Outdoor_Testing.html", self.result)

    def Single_Outdoor_Testing(self, request):
        if request.method == 'POST':
            TransactionProcessing = OutdoorModel()
            result = TransactionProcessing.TransactionProcessing(request, isSingle=True)
            self.result.update(result)
            return JsonResponse(self.result, safe=False)
           # return render(request, "Single_Outdoor_Testing.html", context=self.result)
        else:
            return render(request, "Single_Outdoor_Testing.html", self.result)
