import motor.motor_asyncio


class DB:

    config: object
    dbClient: object
    pdb: object

    __conection = None

    def __init__(self, config):
        global connection
        self.config = config
        self.dbClient = motor.motor_asyncio.AsyncIOMotorClient(self.config['mongodbUrl'])
        connection = self.dbClient.azPrices






