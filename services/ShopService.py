from dbConnectivity.MongoDriver import MongoHandler
from repositories.ArticleRepository import ArticleRepository


class ShopService: #future facade for all operations on shop database
    def __init__(self):
        self._mongoHandler: MongoHandler = MongoHandler()
        self._articlesMongoHandler = self._mongoHandler.articlesHandler
        self._workersMongoHandler = self._mongoHandler.workersHandler
        self._clientsMongoHandler = self._mongoHandler.clientsHandler

        self_articleRepository = ArticleRepository(self._articlesMongoHandler)
