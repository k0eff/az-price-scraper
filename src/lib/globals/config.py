import json

class Config():

    configFile = open('./config.json')
    configData = json.load(configFile)
