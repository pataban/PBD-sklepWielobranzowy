from dbConnectivity.MongoConnector import MongoConnector
from dbConnectivity.MysqlConnector import *
import sqlalchemy as sqla
from repositories.ArticleRepository import ArticleRepository
from repositories.ClientRepository import ClientRepository
from repositories.WorkerRepository import WorkerRepository
from services.ShopService import ShopService
from userInterface.GUI import GUI

if __name__ == "__main__":
    mysqlConnector = MysqlConnector()
    #articleRepository = ArticleRepository(mysqlConnector.articlesHandler)
    #workerRepository = WorkerRepository(mysqlConnector.workersHandler)
    #clientRepository = ClientRepository(mysqlConnector.clientsHandler)
    #shopService = ShopService(articleRepository, workerRepository, clientRepository)


    # uzytkownik testowy
    session=sqla.orm.sessionmaker(bind=mysqlConnector.workersHandler)()
    if not session.query(WorkerORM).count():
        session.add(WorkerORM(id=111,workerNr=111, firstName="aaa", secondName="aaa", 
                login="aaa", password="aaa", isSeller=True, isManager=True, isOwner=True))

    print("towary:")
    tow = session.query(ArticleORM).all()
    for t in tow:
        print(str(t))

    print("pracownicy:")
    pra = session.query(WorkerORM).all()
    for p in pra:
        print(str(p))

    print("klienci:")
    kli=session.query(ClientORM).all()
    for k in kli:
        print(str(k))
        
    session.commit()
    session.close()

    #shopService.delAll()
    #shopService.chkTestUser()
    #shopService.printAll()

    #gui=GUI(shopService)
    #gui.mainloop()


