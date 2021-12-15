import pymongo

class DB:

    config: object
    dbClient: object
    pdb: object
    pricesCol: object
    currentCol: object

    __conection = None

    def __init__(self, mongoConfig):
        global connection
        self.config = mongoConfig
        self.dbClient = pymongo.MongoClient(self.config['mongodbUrl'])
        pdb = self.dbClient.azPrices
        pricesCol = self.dbClient.prices
        currentCol = self.dbClient.current






