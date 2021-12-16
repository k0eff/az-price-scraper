import json
from copy import deepcopy

import logging
from pydantic import BaseModel



log = logging.getLogger("MAIN")
logging.basicConfig()
log.setLevel(logging.INFO)


# Base URL and necessary vars
# baseurl = "https://azure.microsoft.com/api/v2/pricing/virtual-machines-base/calculator/?culture=en-us&discount=mosp"

class Sanitiser:

    prices: object

    def __init__(self, pricesCol) -> None:
        self.prices = pricesCol


    # Results now usable within the dataset object, this is necessary as we need to convert the array of combined API calls back to one JSON object
    def fetchDataset(self):
        lastBatch = None
        records = []
        cursor = self.prices.find().sort("bedeExtraData.currentDate", -1).limit(1)
        for each in cursor:
            records.append(each)
        if len(records) > 0:
            lastBatch = records[0]['bedeExtraData']['batch']

        filter = {}
        if lastBatch != None:
            filter = {"bedeExtraData.batch": lastBatch}

        res = []
        cursor2 = self.prices.find(filter)
        for each in cursor2:
            res.append(each)

        return res

    def sanitiseData(self, nspec):
        dataset = self.fetchDataset()
        dataSetCopy = deepcopy(dataset)
        filteredData = []

        for each in dataset:
            if (nspec.OS not in each['offerName']) \
            or (nspec.Spot not in each['offerName']) \
            or (each['cores']<nspec.minCPU or each['cores']>nspec.maxCPU) \
            or (each['ram']<nspec.minRAM or each['ram']>nspec.maxRAM) \
            or (each['series'] in nspec.excludedSeries):
                continue
            else:
                filteredData.append(each)

        return filteredData

    # Based on what our maximum cpu per node is we can calculate the most efficient config
    def algorithm(self, dataset, nspec):
        bestPrice = 99999999999
        bestOffering = {}
        for each in dataset:
            mutliplier = nspec.maxCPU / each['cores']
            price = float(each['prices']['europe-north']['value']) * mutliplier

            if(price < bestPrice):
                bestPrice = price
                bestOffering = {
                    **bestOffering,
                    "cores": each['cores'],
                    "ram": each['ram'],
                    "diskSize": each['diskSize'],
                    "series": each['series'],
                    "isVcpu": each['isVcpu'],
                    "offerName": each['offerName'],
                    "price": each['prices']['europe-north']['value']
                }

        return bestOffering

