import json
from bson.json_util import dumps

def jsonOut(o):
    return json.loads(dumps(o))