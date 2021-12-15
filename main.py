import json
from src.lib.apiResponse import apiResponse
from src.lib.db import db
from src.api import api
from src.lib.globals.config import Config
from src.lib.handlers import dataHandler as dh


conf = Config()
database = db.DB(mongoConfig=conf.configData)
dataHandler = dh.DataHandler(dbCon=database.dbClient)
app = api.__init__(dh=dataHandler)


