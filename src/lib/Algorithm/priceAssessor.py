import json
from copy import deepcopy

import logging
from pydantic import BaseModel

from src.util.dataTypes.dataTypes import falsey, truthy



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
        filteredData = []

        for each in dataset:
            if (bool(nspec.os) and nspec.os not in each['offerName']) \
            or ((truthy(nspec.spot) and "perhourspot" not in each['prices'])
                or (falsey(nspec.spot) and "perhour" not in each['prices'])
            ) \
            or ("cores" not in each or (each['cores'] < nspec.mincpu or each['cores']>nspec.maxcpu)) \
            or ("ram" not in each or (each['ram']<nspec.minram or each['ram']>nspec.maxram)) \
            or ("series" not in each or (each['series'] in nspec.excluded)):
                continue
            else:
                filteredData.append(each)

        return filteredData

    # Based on what our maximum cpu per node is we can calculate the most efficient config
    def algorithm(self, dataset, nspec):
        bestPrice = 99999999999
        bestOffering = {}
        for cOffer in dataset:
            multiplier = nspec.maxcpu / cOffer['cores']
            if (self.missingPrices(cOffer) or \
                self.missingSpotPrices(cOffer, nspec) or \
                self.missingRegularPrices(cOffer, nspec) or \
                self.missingSpotPricesForMyRegion(cOffer, nspec) or \
                self.missingRegularPricesForMyRegion(cOffer, nspec)
                ): continue
            price = self.getPriceForMyRegion(cOffer, nspec, multiplier)

            if(price < bestPrice):
                bestPrice = price
                bestOffering = {
                    **bestOffering,
                    "cores": cOffer['cores'],
                    "ram": cOffer['ram'],
                    "diskSize": cOffer['diskSize'],
                    "series": cOffer['series'],
                    "isVcpu": cOffer['isVcpu'],
                    "offerName": cOffer['offerName'],
                    "price": price,
                    "region": nspec.region,
                    "spot": nspec.spot
                }

        return bestOffering

    def getPriceForMyRegion(self, offer, nspec, multiplier):
        spotOrNonSpotPrice = 'perhourspot' if truthy(nspec.spot) else "perhour"
        return float(offer['prices'][spotOrNonSpotPrice][nspec.region]['value']) * multiplier

    def missingPrices(self, offer):
        return 'prices' not in offer

    def missingSpotPrices(self, offer, nspec):
        return (truthy(nspec.spot) and 'perhourspot' not in offer['prices'])

    def missingRegularPrices(self, offer, nspec):
        return (falsey(nspec.spot) and 'perhour' not in offer['prices'])

    def missingSpotPricesForMyRegion(self, offer, nspec):
        return (truthy(nspec.spot) and nspec.region not in offer['prices']['perhourspot'])

    def missingRegularPricesForMyRegion(self, offer, nspec):
        return (falsey(nspec.spot) and nspec.region not in offer['prices']['perhour'])
    