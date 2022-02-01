from dbConnectivity.MysqlConnector import BillORM
from models.PaymentMethod import PaymentMethod


class BillDto:
    def __init__(self, bill_orm: BillORM):

        self.billNr = bill_orm.billNr
        self.worker_id = bill_orm.worker_id
        self.paymentMethod = bill_orm.paymentMethod
        self.isAlreadyPaid = bill_orm.isAlreadyPaid
        self.dateTime = bill_orm.dateTime
        self.client_id = bill_orm.client_id

    def __str__(self) -> str:
        return 'BillDto {' + \
               'billNr: ' + str(self.billNr) + \
               ', worker_id: ' + str(self.worker_id) + \
               ', paymentMethod: ' + str(self.paymentMethod) + \
               ', isAlreadyPaid: ' + str(self.isAlreadyPaid) + \
               ', dateTime: ' + str(self.dateTime) + \
               ', client_id: ' + str(self.client_id) + \
               '}'

    def toORM(self):
        pass
