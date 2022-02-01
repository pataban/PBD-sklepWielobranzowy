from dbConnectivity.MysqlConnector import BillORM
from models.PaymentMethod import PaymentMethod


class BillDto:
    def __init__(self, bill_orm: BillORM):

        self.billNr = bill_orm.billNr
        self.worker_id = bill_orm.worker_id
        if bill_orm.paymentMethod == 'CASH':
            self.paymentMethod = PaymentMethod.CASH
        elif bill_orm.paymentMethod == 'BANK_TRANSFER':
            self.paymentMethod = PaymentMethod.BANK_TRANSFER
        else:
            self.paymentMethod = None
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

    @classmethod
    def fromORM(cls, bill_orm):
        pass

    def toORM(self):
        pass
