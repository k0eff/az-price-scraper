from datetime import datetime
from src.util.json.parse import jsonOut
import json
import requests

db = None

class DataHandler:

    prices = None
    config = None

    def __init__(self, pricesCol, cfg) -> None:
        global prices, config
        prices = pricesCol
        config = cfg


    def getAllPrices(self):
        all = []
        cursor = prices.find()
        for each in cursor:
            all.append(each)
        return jsonOut(all)

    def downloadPrices(self):
        baseurl = config['azPriceUrl']
        keepPolling = True
        dataSet = []
        batch = 0

        # Work around for MS only returning 100 results at a time
        while(keepPolling == True):
            list = []
            enrichedData = {
                "bedeExtraData": {
                    "currentDate": datetime.now().isoformat()
                }
            }
            url = baseurl + str(batch)
            result = requests.get(url).json()

            if (len(result['Items']) > 0):
                for each in result['Items']:
                    each = {**each, **enrichedData }
                    list.append(each)
                prices.insert_many(list)

            dataSet.append(result)


            # Loop until there is no longer an extra 100 results remaining
            if(result['Count'] != 100):
                keepPolling = False

            # Increment in batches of 100
            batch += 100
        return True