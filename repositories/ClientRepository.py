from typing import Optional

import pymongo
import sqlalchemy.orm
from bson import ObjectId

from models import NewBillDto
from models.ArticleInBillDto import ArticleInBillDto
from models.Bill import Bill
from models.BillDto import BillDto
from models.ClientOnlyDto import ClientOnlyDto
from models.ClientWithBillsNumbersOnlyDto import ClientWithBillsNumbersOnlyDto
from models.Client import Client

from dbConnectivity.MysqlConnector import *


class ClientRepository:
    def __init__(self, mysqlHandler):
        self._mysql_handler = mysqlHandler

    def findClientOnlyDto(self) -> [ClientOnlyDto]:  # wszyscy klienci bez rachunków
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        client_only_dtos = []
        for client_orm in session.query(ClientORM).all():
            client_only_dtos.append(ClientOnlyDto(client_orm))
        session.close()
        return client_only_dtos

    def findClientOnlyDtoByClientNr(self, clientNr: int) -> Optional[ClientOnlyDto]:
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        client_orm = session.query(ClientORM).filter_by(clientNr=clientNr).one()
        session.close()
        if client_orm is None:
            return None
        return ClientOnlyDto(client_orm)

    def findClientOnlyDtoByVatId(self, vatId: str) -> Optional[ClientOnlyDto]:
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        client_orm = session.query(ClientORM).filter_by(vatId=vatId).one()
        session.close()
        if client_orm is None:
            return None
        return ClientOnlyDto(client_orm)

    def findByIdClientWithBillsNumbersOnlyDto(
            self, client_id) -> Optional[ClientWithBillsNumbersOnlyDto]:  # jeden klient tylko z listą numerów rachunków
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        client_orm = session.query(ClientORM).filter_by(id=client_id).one()
        session.close()
        if client_orm is None:
            return None
        return ClientWithBillsNumbersOnlyDto(client_orm)

    def findBillDto(self) -> [
        BillDto]:  # wszystkie rachunki w postaci rachunku z artykułami w postaci samych id
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        bill_dtos = []
        for bill_orm in session.query(BillORM).all():
            bill_dtos.append(BillDto(bill_orm))
        session.close()
        return bill_dtos
        pass

    def insert(self, newClient: Client) -> bool:
        if newClient is None:
            raise TypeError('Argument newClient cannot be None')
        if not isinstance(newClient, Client):
            raise TypeError('Argument newClient must by of type Client')
        if newClient.object_id is not None:
            raise ValueError('New article cannot have assigned id')

        session = sqla.orm.sessionmaker(self._mysql_handler)()
        client_orm = newClient.toORM()
        session.add(client_orm)
        session.commit()
        inserted_id = client_orm.id
        session.close()
        if inserted_id is None:
            return False
        newClient.object_id = inserted_id
        return True

    def update(self, updatedClient: ClientOnlyDto) -> bool:
        session = sqla.orm.sessionmaker(self._mysql_handler)()
        clientOrm = session.query(ClientORM).filter_by(clientNr=updatedClient.clientNr).one()
        clientOrm.updateByDto(updatedClient)
        session.commit()
        session.close()
        return True

    def remove(self, client_id: str) -> bool:

        pass

    def addNewBill(self, newBill: NewBillDto, products: [ArticleInBillDto]) -> BillORM:
        session = sqla.orm.sessionmaker(self._mysql_handler, autoflush=False)()
        client_orm = session.query(ClientORM).filter_by(clientNr=newBill.client_number).one()
        worker_orm = session.query(WorkerORM).filter_by(workerNr=newBill.worker_number).one()

        newBillOrm = BillORM(
            None,
            self.maxBillNr()+1,
            newBill.isAlreadyPaid,
            newBill.dateTime,
            newBill.paymentMethod,
            newBill.worker_number,
            newBill.client_number,
            []
        )

        session.add(newBillOrm)
        client_orm.addNewBill(newBillOrm)
        worker_orm.addNewBill(newBillOrm)

        session.flush()
        session.commit()
        inserted_id = newBillOrm.id
        if inserted_id is None:
            return None
        session.close()
        return newBillOrm


    def maxClientNr(self) -> int:
        session = sqla.orm.sessionmaker(bind=self._mysql_handler)()
        for result in session.query(ClientORM).order_by(ClientORM.clientNr.desc()).all():
            if result.clientNr is not None:
                session.close()
                return result.clientNr
        session.close()
        return -1

    def maxBillNr(self) -> int:
        session = sqla.orm.sessionmaker(bind=self._mysql_handler)()
        for result in session.query(BillORM).order_by(BillORM.billNr.desc()).all():
            if result.billNr is not None:
                session.close()
                return result.billNr
        session.close()
        return -1
