from dbConnectivity.MongoConnector import MongoConnector
from repositories.ArticleRepository import ArticleRepository
from repositories.ClientRepository import ClientRepository
from repositories.WorkerRepository import WorkerRepository
from services.ShopService import ShopService
from userInterface.GUI import GUI

if __name__ == "__main__":
    mongoConnector = MongoConnector()
    articleRepository = ArticleRepository(mongoConnector.articlesHandler)
    workerRepository = WorkerRepository(mongoConnector.workersHandler)
    clientRepository = ClientRepository(mongoConnector.clientsHandler)
    shopService = ShopService(articleRepository, workerRepository, clientRepository)
    GUI(shopService)
