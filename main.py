import json
from src.lib.apiResponse import apiResponse
from src.lib.db import db
from src.api import api
import uvicorn



configFile = open('./config.json')
configData = json.load(configFile)


from src.lib.db import db
db = db.DB(configData)

api(db, config)

# bla = db.dbClient.bla.blaCol.find({"hello": "world"})

uvicorn.run("app.api:app", host="0.0.0.0", port=8080, reload=True)

 