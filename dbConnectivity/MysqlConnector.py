from pymongo import MongoClient
import sqlalchemy as sqla

from models.ClientOnlyDto import ClientOnlyDto
from models.PaymentMethod import PaymentMethod
# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import relationship, sessionmaker

dbHost = "127.0.0.1"
dbPort = 3306
dbName = "sklepWielobranzowy"  # sklepWielobranzowy
dbPass = "test"
dbstr = f"mysql+pymysql://root:{dbPass}@{dbHost}:{dbPort}/{dbName}"
BazaModel = declarative_base()


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
    id = sqla.Column(sqla.Integer, primary_key=True)
    code = sqla.Column(sqla.Integer, nullable=False)
    name = sqla.Column(sqla.String(255), nullable=False)
    price = sqla.Column(sqla.DECIMAL(10, 2), nullable=False)
    positions = sqla.orm.relationship('PositionORM')  # backref='articles' back_populates='article'

    def update(self, updatedArticle):  # przyjmuje ArticleORM
        self.id = updatedArticle.id
        self.code = updatedArticle.code
        self.name = updatedArticle.name
        self.price = updatedArticle.price
        self.positions = updatedArticle.positions

    def addNewPosition(self, positionOrm):
        if self.positions is not None:
            self.positions.append(positionOrm)
        else:
            self.positions = [positionOrm]

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
        self.workerNr=updatedWorker.workerNr
        self.firstName=updatedWorker.firstName
        self.secondName=updatedWorker.secondName
        self.isSeller=updatedWorker.isSeller
        self.isManager=updatedWorker.isManager
        self.isOwner=updatedWorker.isOwner

    def addNewBill(self, billOrm):
        if self.bills is not None:
            self.bills.append(billOrm)
        else:
            self.bills = [billOrm]

    def __str__(self) -> str:
        return str(vars(self))


class ClientORM(BazaModel):
    __tablename__ = 'clients'
    id = sqla.Column(sqla.Integer, primary_key=True)
    clientNr = sqla.Column(sqla.Integer, nullable=True)
    firstName = sqla.Column(sqla.String(30), nullable=True)
    secondName = sqla.Column(sqla.String(30), nullable=True)
    vatId = sqla.Column(sqla.String(30), nullable=True)
    name = sqla.Column(sqla.String(30), nullable=True)
    telephone = sqla.Column(sqla.String(15), nullable=True)
    address = sqla.Column(sqla.String(100), nullable=True)
    bills = sqla.orm.relationship('BillORM')  # backref='clients' back_populates='client'

    def __init__(self, client_id, clientNr, firstName, secondName, vatId, name, telephone, address, bills):
        self.id = client_id
        self.clientNr = clientNr
        self.firstName = firstName
        self.secondName = secondName
        self.vatId = vatId
        self.name = name
        self.telephone = telephone
        self.address = address
        self.bills = bills

    def addNewBill(self, billOrm):
        if self.bills is not None:
            self.bills.append(billOrm)
        else:
            self.bills = [billOrm]

    def updateByDto(self, clientOnlyDto):
        self.firstName = clientOnlyDto.firstName
        self.secondName = clientOnlyDto.secondName
        self.name = clientOnlyDto.name
        self.telephone = clientOnlyDto.telephone
        self.vatId = clientOnlyDto.vatId
        self.address = clientOnlyDto.address
        self.clientNr = clientOnlyDto.clientNr
        self.id = clientOnlyDto.object_id


    def __str__(self) -> str:
        return str(vars(self))


class BillORM(BazaModel):
    __tablename__ = 'bills'
    id = sqla.Column(sqla.Integer, primary_key=True)
    billNr = sqla.Column(sqla.Integer, nullable=False)
    isAlreadyPaid = sqla.Column(sqla.Boolean, default=False)
    dateTime = sqla.Column(sqla.String(30), nullable=False)
    paymentMethod = sqla.Column(sqla.Enum(PaymentMethod), default=PaymentMethod.CASH)
    worker_id = sqla.Column(sqla.Integer, sqla.ForeignKey('workers.id'))
    client_id = sqla.Column(sqla.Integer, sqla.ForeignKey('clients.id'))
    positions = sqla.orm.relationship('PositionORM')  # backref='bills' back_populates='bill'

    def __init__(self, bill_id, billNr, isAlreadyPaid, dateTime, paymentMethod, worker_id, client_id, positions):
        self.id = bill_id
        self.billNr = billNr
        self.isAlreadyPaid = isAlreadyPaid
        self.dateTime = dateTime
        self.paymentMethod = paymentMethod
        self.worker_id = worker_id
        self.client_id = client_id
        self.positions = positions

    def __str__(self) -> str:
        return str(vars(self))


class PositionORM(BazaModel):
    __tablename__ = 'positions'
    article_id = sqla.Column(sqla.Integer, sqla.ForeignKey('articles.id'), primary_key=True)
    bill_id = sqla.Column(sqla.Integer, sqla.ForeignKey('bills.id'), primary_key=True)
    quantity = sqla.Column(sqla.Integer, default=1)
    purchasePrice = sqla.Column(sqla.DECIMAL(10, 2), nullable=False)

    def __init__(self, article_id, bill_id, quantity, purchasePrice):
        self.article_id = article_id
        self.bill_id = bill_id
        self.quantity = quantity
        self.purchasePrice = purchasePrice

    def __str__(self) -> str:
        return str(vars(self))
