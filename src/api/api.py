from src.lib import apiResponse
from src.lib.handlers import dataHandler
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI


app = None
dataHandler = None

def __init__(dh):
    global dataHandler, app
    app = FastAPI()
    dataHandler = dh

    @app.get(path="/")
    def getData():
        data = dataHandler.getTestDbData()
        return {"abv":"dge"}
    return app

