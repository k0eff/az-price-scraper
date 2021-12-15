

async def getTestDbData(dbCon):
    res = await dbCon.bla.blaCol.find({"hello": "world"})
    return res
