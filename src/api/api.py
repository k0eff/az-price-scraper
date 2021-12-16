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


    @app.post(path="/prices")
    def putData():
        data=dataHandler.downloadPrices()
        return {"success": True}


    @app.get(path="/prices")
    def getData():
        data = dataHandler.getAllPrices()
        return data


    @app.get(path="/price")
    def getBestOffering(mincpu="", maxcpu="", minram="", maxram="", os="", spot="", excluded=""):
        params = { 
            "mincpu": mincpu, 
            "maxcpu": maxcpu, 
            "minram": minram, 
            "maxram": maxram, 
            "os": os, 
            "spot": spot, 
            "excluded": excluded
        }
        data = dataHandler.getBestOffering(params)
        return data


    return app
