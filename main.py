import json
from src.lib.apiResponse import apiResponse
from src.lib.db import db
from src.api import api
from src.lib.globals.config import Config
from src.lib.repositories.dataRepo import DataRepo


conf = Config().configData
database = db.DB(mongoConfig=conf)
dataRepo = DataRepo(pricesCol=database.pricesCol, bestOffersCol=database.bestOffers, cfg=conf)
app = api.init(dr=dataRepo)


