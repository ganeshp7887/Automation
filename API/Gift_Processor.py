from API.Utility import Utility

class Gift_processor:

    @staticmethod
    def BlackHawkUpc_finder(cardnumber):
        data = Utility.readGiftBins()
        rootNode = next(iter(data))
        return data.get(rootNode).get(cardnumber, "00000000000")