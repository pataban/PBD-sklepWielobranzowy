from pymongo import MongoClient
import sqlalchemy as sqla
from models.PaymentMethod import PaymentMethod
#from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, sessionmaker

dbHost="127.0.0.1"
dbPort=3306
dbName="sklepWielobranzowy"#sklepWielobranzowy
dbstr=f"mysql+pymysql://root:@{dbHost}:{dbPort}/{dbName}"
BazaModel=declarative_base()

class MysqlConnector:
    def __init__(self):
        self._client = None
        self._db = sqla.create_engine(dbstr)
        self.articlesHandler = self._db
        self.workersHandler = self._db
        self.clientsHandler = self._db
        BazaModel.metadata.create_all(self._db)



class ArticleORM(BazaModel):
    __tablename__ = 'articles'
    id=sqla.Column(sqla.Integer, primary_key=True)
    code=sqla.Column(sqla.Integer,nullable=False)
    name=sqla.Column(sqla.String(255),nullable=False)
    price=sqla.Column(sqla.DECIMAL(10,2),nullable=False)
    positions = sqla.orm.relationship('PositionORM')#backref='articles' back_populates='article'

    def update(self,updatedArticle):#przyjmuje ArticleORM
        self.id=updatedArticle.id
        self.code=updatedArticle.code
        self.name=updatedArticle.name
        self.price=updatedArticle.price
        self.positions=updatedArticle.positions
    
    def __str__(self) -> str:
        return str(vars(self))


class WorkerORM(BazaModel):
    __tablename__ = 'workers'
    id=sqla.Column(sqla.Integer,primary_key=True)
    workerNr=sqla.Column(sqla.Integer,nullable=False)
    firstName=sqla.Column(sqla.String(30),nullable=False)
    secondName=sqla.Column(sqla.String(30),nullable=False)
    login=sqla.Column(sqla.String(30),nullable=False)
    password=sqla.Column(sqla.String(30),nullable=False)
    isSeller=sqla.Column(sqla.Boolean,default=False)
    isManager=sqla.Column(sqla.Boolean,default=False)
    isOwner=sqla.Column(sqla.Boolean,default=False)
    bills=sqla.orm.relationship('BillORM')#backref='workers' back_populates='worker'
    
    def update(self,updatedWorker):#przyjmuje WorkerORM
        self.id=updatedWorker.id
        self.code=updatedWorker.code
        self.name=updatedWorker.name
        self.price=updatedWorker.price
        self.positions=updatedWorker.positions

    def __str__(self) -> str:
        return str(vars(self))
        

class ClientORM(BazaModel):
    __tablename__ = 'clients'
    id = sqla.Column(sqla.Integer,primary_key=True)
    clientNr = sqla.Column(sqla.Integer,nullable=True)
    firstName = sqla.Column(sqla.String(30),nullable=True)
    secondName = sqla.Column(sqla.String(30),nullable=True)
    vatId = sqla.Column(sqla.String(30),nullable=True)
    name = sqla.Column(sqla.String(30),nullable=True)
    telephone = sqla.Column(sqla.String(15),nullable=True)
    address = sqla.Column(sqla.String(100),nullable=True)
    bills=sqla.orm.relationship('BillORM')#backref='clients' back_populates='client'

    def __str__(self) -> str:
        return str(vars(self))
    

class BillORM(BazaModel):
    __tablename__ = 'bills'
    id = sqla.Column(sqla.Integer,primary_key=True)
    billNr = sqla.Column(sqla.Integer,nullable=False)
    isAlreadyPaid = sqla.Column(sqla.Boolean,default=False)
    dateTime = sqla.Column(sqla.String(30),nullable=False)
    paymentMethod = sqla.Column(sqla.Enum(PaymentMethod),default=PaymentMethod.CASH)
    worker = sqla.Column(sqla.Integer,sqla.ForeignKey('workers.id'))
    client = sqla.Column(sqla.Integer,sqla.ForeignKey('clients.id'))
    positions = sqla.orm.relationship('PositionORM')#backref='bills' back_populates='bill'

    def __str__(self) -> str:
        return str(vars(self))


class PositionORM(BazaModel):
    __tablename__ = 'positions'
    article = sqla.Column(sqla.Integer,sqla.ForeignKey('articles.id'),primary_key=True)
    bill = sqla.Column(sqla.Integer,sqla.ForeignKey('bills.id'),primary_key=True)
    quantity = sqla.Column(sqla.Integer,default=1)
    purchasePrice = sqla.Column(sqla.DECIMAL(10,2),nullable=False)

    def __str__(self) -> str:
        return str(vars(self))
    

