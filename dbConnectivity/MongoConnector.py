from pymongo import MongoClient


class MongoConnector:

    def __init__(self):
        self._client = MongoClient("mongodb://localhost:27017")
        # mongodb://myDBReader:D1fficultP%40ssw0rd@DBAddress:27017/?authSource=admin
        self._db = self._client.sklepWielobranzowy
        self.articlesHandler = self._db.articles
        self.workersHandler = self._db.workers
        self.clientsHandler = self._db.clients
