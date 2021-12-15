import pymongo

class DB:

    config: object
    dbClient: object
    dbName: str
    pdb: object
    pricesCol: object
    currentCol: object

    __conection = None

    def __init__(self, mongoConfig):
        self.config = mongoConfig
        self.dbClient = pymongo.MongoClient(self.config['mongodbUrl'])
        self.dbName = self.config['mongoDbName']
        self.pdb = self.dbClient[self.dbName]
        self.pricesCol = self.pdb.prices
        self.currentCol = self.pdb.current






