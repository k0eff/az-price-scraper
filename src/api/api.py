import FastAPI
from lib.apiResponse import apiResponse
from src.lib.handlers import dataHandler

app = FastAPI

dbClient = None
config = None
dbInstance = None

def setup(dbClient, config):
    dbClient = dbClient
    config = config

    return dbClient, config



@app.get("/", response_description="test route", response_model=apiResponse)
async def getData():
    global dbClient
    return await dataHandler.getTestDbData(dbClient)

