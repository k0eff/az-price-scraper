import json

class Config():

    configFile = open('./config.json')
    configData = json.load(configFile)

    from src.lib.db import db
    db = db.DB(configData)