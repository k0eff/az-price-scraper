from datetime import datetime
from src.util.json.parse import jsonOut
import json
import requests
from uuid import uuid4
from src.lib.Algorithm.priceAssessor import Sanitiser 
from src.models.nodeSpecification import NodeSpecification

db = None

class DataRepo:

    prices = None
    bestOffers = None
    config = None

    def __init__(self, pricesCol, bestOffersCol, cfg) -> None:
        global prices, config, bestOffers
        prices = pricesCol
        bestOffers = bestOffersCol
        config = cfg


    def getAllPrices(self):
        all = []
        cursor = prices.find()
        for each in cursor:
            all.append(each)
        return jsonOut(all)

    def downloadPrices(self):
        baseurl = config['azPriceUrl']

        enrichedData = {
            "bedeExtraData": {
                "extractionDate": datetime.now().isoformat(),
                "batch": str(uuid4())
            }
        }

        list = []

        url = baseurl
        result = requests.get(url).json()
        if bool(result) and len(result['offers']) > 0:
            items = result['offers'].items()
            for k, v in items:
                res = {**v, **enrichedData, **{"offerName": k} }
                list.append(res)
            prices.insert_many(list)

        return True

    def getBestOffering(self, params):
        nodeSpec = NodeSpecification(params)
        sanitiser = Sanitiser(pricesCol=prices)
        dataset = sanitiser.sanitiseData(nodeSpec)
        bestVmType = sanitiser.algorithm(dataset, nodeSpec)
        return bestVmType

    def saveBestOffering(self, record):
        bestOffers.insert_one(record)
        return