from django.shortcuts import render
from API.Utility import Utility

class Single_Instore_Testing:

    def __init__(self):
        self.result = {}
        context = {
            "Transactions" : Utility.readTransactionTypes(),
        }
        self.result.update(context)


    def Single_Instore_Testing(self, request):
        return render(request, 'Single_Instore_Testing.html', self.result)