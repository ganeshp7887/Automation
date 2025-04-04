from django.http import JsonResponse
from django.shortcuts import render
from API.Utility import Utility
from .models import InstoreModel


class InstoreTesting:

    def __init__(self):
        self.result  = {
            "Transactions" : Utility.readTransactionTypes().get("Instore_Transactions"),
        }

    def bypass(self, request):
        bypass = InstoreModel().bypassModel()
        self.result = {
            "data" : bypass
        }
        return JsonResponse(self.result, safe=False)

    def Instore_Testing(self, request):
        if request.method == 'POST':
            TransactionProcessing = InstoreModel()
            result = TransactionProcessing.TransactionProcessing(request, False)
            self.result.update(result)
            return JsonResponse(self.result, safe=False)
        else:
            return render(request, 'Instore_Testing.html',  self.result)

    def Single_Instore_Testing(self, request):
        if request.method == 'POST':
            TransactionProcessing = InstoreModel()
            result = TransactionProcessing.TransactionProcessing(request, True)
            self.result.update(result)
            return JsonResponse(self.result, safe=False)
        else:
            return render(request, 'Single_Instore_Testing.html',  self.result)