from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI


app = None
dataRepo = None

def init(dr):
    global dataRepo, app
    app = FastAPI()
    dataRepo = dr


    @app.post(path="/prices")
    def putData():
        data=dataRepo.downloadPrices()
        return {"success": True}


    @app.get(path="/prices")
    def getData():
        data = dataRepo.getAllPrices()
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
        data = dataRepo.getBestOffering(params)
        return data


    return app
