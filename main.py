import json
from src.lib.apiResponse import apiResponse
from src.lib.db import db
from src.api import api
import uvicorn
from src.lib.globals.config import Config

api(db, config)

# bla = db.dbClient.bla.blaCol.find({"hello": "world"})

uvicorn.run("app.api:app", host="0.0.0.0", port=8080, reload=True)

 