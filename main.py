import json

import requests
import logging

# Init Logger
log = logging.getLogger("MAIN")
logging.basicConfig()
log.setLevel(logging.INFO)

# Base URL and necessary vars
baseurl = "https://prices.azure.com/api/retail/prices?$filter=endswith(meterName, 'Spot') and armRegionName eq 'northeurope'&$skip="
keepPolling = True
dataSet = []
batch = 0

# Work around for MS only returning 100 results at a time
while(keepPolling == True):
    url = baseurl + str(batch)
    log.info(url)
    result = requests.get(url).json()
    dataSet.append(result)

    # Loop until there is no longer an extra 100 results remaining
    if(result['Count'] != 100):
        keepPolling = False

    # Increment in batches of 100
    batch += 100

# Write dataset to file (for debugging)
with open('dataset.json', 'w') as f:
    json.dump(dataSet, f)

# Results now usable within the dataset object, this is necessary as we need to convert the array of combined API calls back to one JSON object
dataSet = json.dumps(dataSet)
dataset = json.loads(dataSet)