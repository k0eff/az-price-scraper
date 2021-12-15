import motor.motor_asyncio


class DB:

    config: object
    dbClient: object
    pdb: object



    def __init__(self, config):
        self.config = config
        self.dbClient = motor.motor_asyncio.AsyncIOMotorClient(self.config['mongodbUrl'])
        pdb = self.dbClient.azPrices






