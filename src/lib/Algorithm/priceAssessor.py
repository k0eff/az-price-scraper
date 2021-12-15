import json
from copy import deepcopy

import logging
from pydantic import BaseModel

# Init Logger
from src.models.node import Node
from src.models.nodeSpecification import NodeSpecification

log = logging.getLogger("MAIN")
logging.basicConfig()
log.setLevel(logging.INFO)


# Base URL and necessary vars
# baseurl = "https://azure.microsoft.com/api/v2/pricing/virtual-machines-base/calculator/?culture=en-us&discount=mosp"

# This class will be used to filter down the dataset before it is handed to the algoirthm

class Sanitiser:

    # Results now usable within the dataset object, this is necessary as we need to convert the array of combined API calls back to one JSON object

    def fetchDataset(self):
        with open("dataset.json", "r") as i:
            JSON_data = i.read()
            dataset = json.loads(JSON_data)
        return dataset

    def sanitiseData(self, nspec):
        dataset = self.fetchDataset()
        dataSetCopy = deepcopy(dataset)

        for k,v in dataSetCopy['offers'].items():
            # Remove non-relevant OS, remove non spot
            if (nspec.OS not in k):
                del dataset['offers'][k]
                continue

            if(nspec.Spot not in k):
                del dataset['offers'][k]
                continue

            if(v['cores']<nspec.minCPU or v['cores']>nspec.maxCPU):
                del dataset['offers'][k]
                continue

            if(v['ram']<nspec.minRAM or v['ram']>nspec.maxRAM):
                del dataset['offers'][k]
                continue

            if(v['series'] in nspec.excludedSeries):
                del dataset['offers'][k]
                continue

        return dataset

    # Based on what our maximum cpu per node is we can calculate the most efficient config
    def algorithm(self, dataset, nspec):
        bestPrice = 9999999999
        bestNode = None
        for k,v in dataset['offers'].items():
            mutliplier = nspec.maxCPU / v['cores']
            price = int(v['prices']['europe-north']['value']) * mutliplier

            if(price < bestPrice):
                bestPrice = price
                bestNode = Node(**v)
                bestNode.name = k
                bestNode.price = v['prices']['europe-north']['value']

        return bestNode

nodeSpec = NodeSpecification()
sanitiser = Sanitiser()
dataset = sanitiser.sanitiseData(nodeSpec)
bestVmType = sanitiser.algorithm(dataset, nodeSpec)
print(bestVmType)