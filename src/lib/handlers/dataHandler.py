import pprint

db = None


class DataHandler:

    db = None

    def __init__(self, dbCon) -> None:
        global db
        db = dbCon


    def getTestDbData(self):

        all = []
        # cursor = db.bla.blaCol.find({"hello": "world2"})
        cursor = db.bla.blaCol.find().limit(100)
        # bla = db.bla.blaCol.countDocuments()
        for each in cursor:
            pprint("hello")
            all.append(each)
        return all

